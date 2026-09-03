#!/usr/bin/env python3
"""Place ten human voice takes and an optional ducked music bed on the master."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path


STARTS = [0, 10, 24, 40, 58, 80, 100, 118, 140, 154]
SLOTS = [10, 14, 16, 18, 22, 20, 18, 22, 14, 20]
EXTENSIONS = {".wav", ".aiff", ".aif", ".m4a", ".mp3", ".aac", ".flac"}


def duration(path: Path) -> float:
    result = subprocess.run(
        [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "json",
            str(path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(json.loads(result.stdout)["format"]["duration"])


def find_take(directory: Path, number: int) -> Path:
    matches = [
        path
        for path in directory.glob(f"{number:02d}.*")
        if path.suffix.lower() in EXTENSIONS
    ]
    if len(matches) != 1:
        raise SystemExit(
            f"Expected exactly one supported take named {number:02d}.* in {directory}; "
            f"found {len(matches)}."
        )
    return matches[0]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", type=Path, required=True, help="Approved silent visual master")
    parser.add_argument("--takes", type=Path, default=Path("voiceover/takes"))
    parser.add_argument("--music", type=Path, help="Optional music bed, ducked beneath narration")
    parser.add_argument("--output", type=Path, default=Path("renders/pyroscan-webmcp-final.mp4"))
    args = parser.parse_args()

    for binary in ("ffmpeg", "ffprobe"):
        if not shutil.which(binary):
            raise SystemExit(f"{binary} is required but was not found on PATH")
    if not args.video.is_file():
        raise SystemExit(f"Visual master not found: {args.video}")
    if args.music is not None and not args.music.is_file():
        raise SystemExit(f"Music bed not found: {args.music}")

    takes = [find_take(args.takes, index) for index in range(1, 11)]
    for index, (take, slot) in enumerate(zip(takes, SLOTS, strict=True), start=1):
        take_duration = duration(take)
        if take_duration > slot:
            raise SystemExit(
                f"Take {index:02d} is {take_duration:.2f}s but its slot is {slot:.2f}s. "
                "Record a shorter take rather than time-stretching the voice."
            )
        print(f"{index:02d}: {take.name} · {take_duration:.2f}s / {slot:.2f}s")

    visual_duration = duration(args.video)
    args.output.parent.mkdir(parents=True, exist_ok=True)

    filters: list[str] = []
    labels: list[str] = []
    for input_index, start in enumerate(STARTS, start=1):
        label = f"voice{input_index:02d}"
        delay_ms = start * 1000
        filters.append(
            f"[{input_index}:a]aresample=48000,highpass=f=70,lowpass=f=16000,"
            f"adelay={delay_ms}|{delay_ms}[{label}]"
        )
        labels.append(f"[{label}]")
    voice_mix = (
        "".join(labels)
        + "amix=inputs=10:duration=longest:normalize=0,"
        + "pan=stereo|c0=c0|c1=c0,"
        + "loudnorm=I=-16:TP=-1.5:LRA=7,apad,"
        + f"atrim=duration={visual_duration:.3f}"
    )
    output_label = "voiceout"
    if args.music is None:
        filters.append(voice_mix + "[voiceout]")
    else:
        # Normalize the bed well below the narration, then use the narration as
        # a sidechain key so the music recedes further whenever speech is present.
        filters.append(voice_mix + ",asplit=2[voiceout][voicekey]")
        filters.append(
            f"[11:a]aresample=48000,atrim=duration={visual_duration:.3f},"
            "asetpts=N/SR/TB,afade=t=in:st=0:d=2,afade=t=out:st=169:d=5,"
            "loudnorm=I=-26:TP=-8:LRA=5[musicbase]"
        )
        filters.append(
            "[musicbase][voicekey]sidechaincompress="
            "threshold=.02:ratio=8:attack=25:release=400:makeup=1[ducked]"
        )
        filters.append(
            "[voiceout][ducked]amix=inputs=2:duration=longest:normalize=0:"
            "weights='1 .8',alimiter=limit=.84:level=false,apad[finalout]"
        )
        output_label = "finalout"

    command = ["ffmpeg", "-y", "-i", str(args.video)]
    for take in takes:
        command.extend(["-i", str(take)])
    if args.music is not None:
        command.extend(["-stream_loop", "-1", "-i", str(args.music)])
    command.extend(
        [
            "-filter_complex",
            ";".join(filters),
            "-map",
            "0:v:0",
            "-map",
            f"[{output_label}]",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-ar",
            "48000",
            "-b:a",
            "192k",
            "-t",
            f"{visual_duration:.3f}",
            "-movflags",
            "+faststart",
            str(args.output),
        ]
    )
    subprocess.run(command, check=True)
    print(f"Wrote {args.output} ({duration(args.output):.2f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
