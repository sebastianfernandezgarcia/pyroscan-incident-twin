#!/usr/bin/env python3
"""Generate PyroScan's original, deterministic ambient technology music bed."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=174.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("media-source/pyroscan-tech-bed-original.wav"),
    )
    args = parser.parse_args()

    if not shutil.which("ffmpeg"):
        raise SystemExit("ffmpeg is required but was not found on PATH")
    if args.duration <= 0:
        raise SystemExit("duration must be positive")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    duration = f"{args.duration:.3f}"

    # D-minor/Aeolian drone + sparse four-second pulses. Every oscillator and
    # envelope is authored here, so the result is original and reproducible.
    left = (
        ".10*sin(2*PI*73.416*t)*(0.76+0.24*sin(2*PI*.05*t))"
        "+.065*sin(2*PI*110*t+.25*sin(2*PI*.031*t))"
        "+.040*sin(2*PI*174.614*t)"
        "+.030*sin(2*PI*293.665*t)*exp(-5*mod(t,4))"
        "+.018*sin(2*PI*440*t)*exp(-8*mod(t+2,8))"
    )
    right = (
        ".10*sin(2*PI*73.563*t)*(0.76+0.24*sin(2*PI*.047*t))"
        "+.065*sin(2*PI*109.82*t+.25*sin(2*PI*.029*t))"
        "+.040*sin(2*PI*174.79*t)"
        "+.030*sin(2*PI*293.37*t)*exp(-5*mod(t+.08,4))"
        "+.018*sin(2*PI*439.56*t)*exp(-8*mod(t+2.1,8))"
    )
    synth = f"aevalsrc=exprs='{left}|{right}':s=48000:d={duration}:c=stereo"

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        synth,
        "-f",
        "lavfi",
        "-i",
        f"anoisesrc=color=pink:amplitude=.018:sample_rate=48000:d={duration}",
        "-filter_complex",
        (
            "[0:a]highpass=f=42,lowpass=f=5400,"
            "aecho=.75:.42:760|1510:.12|.07[synth];"
            "[1:a]highpass=f=240,lowpass=f=1450,tremolo=f=.10:d=.45,"
            "volume=.12,pan=stereo|c0=c0|c1=c0[air];"
            "[synth][air]amix=inputs=2:duration=longest:normalize=0,"
            f"atrim=duration={duration},afade=t=in:st=0:d=3,"
            f"afade=t=out:st={max(0.0, args.duration - 6):.3f}:d=6,"
            "alimiter=limit=.90[out]"
        ),
        "-map",
        "[out]",
        "-ar",
        "48000",
        "-ac",
        "2",
        "-c:a",
        "pcm_s24le",
        str(args.output),
    ]
    subprocess.run(command, check=True)
    print(f"Wrote original deterministic technology bed: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
