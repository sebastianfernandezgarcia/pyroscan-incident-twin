#!/usr/bin/env python3
"""Split the approved single-file narration into the ten storyboard slots."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path


# Midpoints of natural pauses in the approved full narration. Keeping half of
# each pause on either side avoids clipped breaths while preserving the voice.
CUTS = [
    (0.000, 6.550),
    (6.550, 18.140),
    (18.140, 27.160),
    (27.160, 42.820),
    (42.820, 57.830),
    (57.830, 70.850),
    (70.850, 84.160),
    (84.160, 100.540),
    (100.540, 110.970),
    (110.970, 130.194),
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("voiceover/takes"))
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required but was not found on PATH")
    if not args.source.is_file():
        raise SystemExit(f"Narration source not found: {args.source}")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "source": str(args.source),
        "sourceSha256": sha256(args.source),
        "method": "natural-pause midpoint cuts; PCM mono 48 kHz",
        "takes": [],
    }

    for index, (start, end) in enumerate(CUTS, start=1):
        output = args.output_dir / f"{index:02d}.wav"
        subprocess.run(
            [
                "ffmpeg",
                "-hide_banner",
                "-loglevel",
                "error",
                "-y",
                "-ss",
                f"{start:.3f}",
                "-to",
                f"{end:.3f}",
                "-i",
                str(args.source),
                "-ac",
                "1",
                "-ar",
                "48000",
                "-c:a",
                "pcm_s24le",
                str(output),
            ],
            check=True,
        )
        take = {
            "number": index,
            "sourceStart": start,
            "sourceEnd": end,
            "duration": round(end - start, 3),
            "path": str(output),
            "sha256": sha256(output),
        }
        manifest["takes"].append(take)
        print(f"{index:02d}: {start:7.3f}–{end:7.3f} → {output.name}")

    manifest_path = args.output_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Wrote {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
