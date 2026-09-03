#!/usr/bin/env python3
"""Generate PyroScan's original, deterministic, musical technology bed."""

from __future__ import annotations

import argparse
import math
import wave
from pathlib import Path

import numpy as np


SAMPLE_RATE = 48_000
BPM = 104.0
BEAT = 60.0 / BPM
BAR = BEAT * 4
RNG_SEED = 20260903


def midi(note: float) -> float:
    """Convert a MIDI note number to frequency in Hz."""

    return 440.0 * 2.0 ** ((note - 69.0) / 12.0)


def envelope(length: int, attack: float, decay: float) -> np.ndarray:
    attack_samples = max(1, min(length, int(attack * SAMPLE_RATE)))
    env = np.exp(-np.arange(length, dtype=np.float32) / max(1.0, decay * SAMPLE_RATE))
    env[:attack_samples] *= np.linspace(0.0, 1.0, attack_samples, dtype=np.float32)
    return env


def add_signal(
    mix: np.ndarray,
    start: float,
    signal: np.ndarray,
    gain: float,
    pan: float = 0.0,
) -> None:
    first = max(0, int(start * SAMPLE_RATE))
    if first >= len(mix):
        return
    signal = signal[: len(mix) - first]
    # Equal-power panning preserves energy while keeping the centre uncluttered.
    angle = (max(-1.0, min(1.0, pan)) + 1.0) * math.pi / 4.0
    mix[first : first + len(signal), 0] += signal * gain * math.cos(angle)
    mix[first : first + len(signal), 1] += signal * gain * math.sin(angle)


def add_pluck(mix: np.ndarray, start: float, note: int, gain: float, pan: float) -> None:
    length = int(0.46 * SAMPLE_RATE)
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    frequency = midi(note)
    # A short glassy stack makes the pattern read as music instead of a drone.
    signal = (
        np.sin(2 * np.pi * frequency * t)
        + 0.34 * np.sin(2 * np.pi * frequency * 2.01 * t + 0.2)
        + 0.13 * np.sin(2 * np.pi * frequency * 3.98 * t + 0.7)
    )
    signal *= envelope(length, attack=0.006, decay=0.16)
    add_signal(mix, start, signal, gain, pan)


def add_bass(mix: np.ndarray, start: float, note: int, gain: float) -> None:
    length = int((BAR * 0.92) * SAMPLE_RATE)
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    frequency = midi(note)
    signal = np.sin(2 * np.pi * frequency * t + 0.07 * np.sin(2 * np.pi * 2.2 * t))
    signal += 0.18 * np.sin(2 * np.pi * frequency * 2 * t)
    signal *= envelope(length, attack=0.035, decay=1.05)
    add_signal(mix, start, signal, gain, 0.0)


def add_pad(mix: np.ndarray, start: float, notes: tuple[int, ...], gain: float) -> None:
    length = int((BAR * 1.12) * SAMPLE_RATE)
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    # float32 sin(pi) can land a few ulps below zero; clamp before the
    # fractional power so the tail never produces NaNs.
    fade = np.clip(
        np.sin(np.linspace(0.0, np.pi, length, dtype=np.float32)),
        0.0,
        None,
    ) ** 1.4
    for index, note in enumerate(notes):
        frequency = midi(note)
        detune = 1.0 + (-0.0015 if index % 2 == 0 else 0.0015)
        signal = np.sin(2 * np.pi * frequency * detune * t)
        signal += 0.16 * np.sin(2 * np.pi * frequency * 2.0 * t + index * 0.5)
        signal *= fade
        pan = -0.55 + (1.1 * index / max(1, len(notes) - 1))
        add_signal(mix, start, signal, gain / len(notes), pan)


def add_kick(mix: np.ndarray, start: float, gain: float) -> None:
    length = int(0.32 * SAMPLE_RATE)
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    phase = 2 * np.pi * (46 * t + (105 - 46) * (1 - np.exp(-t * 22)) / 22)
    signal = np.sin(phase) * np.exp(-t * 15)
    signal += 0.14 * np.sin(2 * np.pi * 180 * t) * np.exp(-t * 45)
    add_signal(mix, start, signal, gain, 0.0)


def add_hat(
    mix: np.ndarray,
    rng: np.random.Generator,
    start: float,
    gain: float,
    pan: float,
) -> None:
    length = int(0.095 * SAMPLE_RATE)
    noise = rng.standard_normal(length).astype(np.float32)
    # First difference removes the low, rough part of the noise.
    bright = np.concatenate(([0.0], np.diff(noise))).astype(np.float32)
    bright *= envelope(length, attack=0.0015, decay=0.027)
    add_signal(mix, start, bright, gain, pan)


def add_clap(mix: np.ndarray, rng: np.random.Generator, start: float, gain: float) -> None:
    length = int(0.22 * SAMPLE_RATE)
    t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
    noise = rng.standard_normal(length).astype(np.float32)
    bright = np.concatenate(([0.0], np.diff(noise))).astype(np.float32)
    bursts = (
        np.exp(-t * 30)
        + 0.62 * np.exp(-np.maximum(0.0, t - 0.026) * 38) * (t >= 0.026)
        + 0.36 * np.exp(-np.maximum(0.0, t - 0.052) * 44) * (t >= 0.052)
    )
    add_signal(mix, start, bright * bursts, gain, 0.08)


def add_transition(mix: np.ndarray, start: float, gain: float) -> None:
    notes = (74, 77, 81, 84)
    for index, note in enumerate(notes):
        add_pluck(
            mix,
            start + index * 0.105,
            note,
            gain * (1.0 - index * 0.1),
            -0.7 + index * 0.46,
        )


def energy_at(second: float) -> float:
    """Scene-aware musical intensity for the ten-film-beat structure."""

    if second < 10:
        return 0.24
    if second < 24:
        return 0.36
    if second < 40:
        return 0.54
    if second < 58:
        return 0.66
    if second < 80:
        return 0.79
    if second < 100:
        return 0.88
    if second < 118:
        return 0.96
    if second < 140:
        return 0.72
    if second < 154:
        return 1.0
    if second < 166:
        return 0.62
    return max(0.12, 0.62 * (174.0 - second) / 8.0)


def render(duration: float) -> np.ndarray:
    sample_count = int(round(duration * SAMPLE_RATE))
    mix = np.zeros((sample_count, 2), dtype=np.float32)
    rng = np.random.default_rng(RNG_SEED)

    # D minor → B-flat → F → C: optimistic motion with a cinematic tech colour.
    chords: tuple[tuple[tuple[int, ...], tuple[int, ...], int], ...] = (
        ((50, 57, 62, 65), (74, 77, 81, 86, 81, 77, 72, 69), 38),
        ((46, 53, 58, 62), (70, 74, 77, 82, 77, 74, 69, 65), 34),
        ((53, 60, 65, 69), (77, 81, 84, 89, 84, 81, 76, 72), 41),
        ((48, 55, 60, 64), (72, 76, 79, 84, 79, 76, 71, 67), 36),
    )

    bars = int(math.ceil(duration / BAR))
    for bar_index in range(bars):
        start = bar_index * BAR
        chord, pattern, bass = chords[bar_index % len(chords)]
        energy = energy_at(start)
        add_pad(mix, start, chord, 0.085 * energy)

        if start >= 18:
            add_bass(mix, start, bass, 0.115 * energy)
            for step, note in enumerate(pattern):
                note_start = start + step * (BEAT / 2)
                if note_start >= duration:
                    break
                accent = 1.22 if step in (0, 4) else 0.86
                pan = -0.48 if step % 2 == 0 else 0.48
                add_pluck(mix, note_start, note, 0.077 * energy * accent, pan)

        if start >= 36:
            for beat_index in range(4):
                beat_start = start + beat_index * BEAT
                kick_gain = (
                    0.14 * energy
                    if beat_index % 2 == 0 or start >= 80
                    else 0.08 * energy
                )
                add_kick(mix, beat_start, kick_gain)
                add_hat(
                    mix,
                    rng,
                    beat_start + BEAT / 2,
                    0.011 * energy,
                    -0.3 if beat_index % 2 == 0 else 0.3,
                )
                if start >= 58 and beat_index in (1, 3):
                    add_clap(mix, rng, beat_start, 0.0065 * energy)

        # A sixteenth-note digital tick adds animation without filling every gap.
        if start >= 40:
            for tick in (1, 3, 6, 9, 11, 14):
                tick_start = start + tick * (BEAT / 4)
                if tick_start >= duration:
                    continue
                length = int(0.028 * SAMPLE_RATE)
                t = np.arange(length, dtype=np.float32) / SAMPLE_RATE
                signal = np.sin(2 * np.pi * (1_450 + 85 * (tick % 3)) * t)
                signal *= np.exp(-t * 115)
                add_signal(
                    mix,
                    tick_start,
                    signal,
                    0.0075 * energy,
                    -0.65 + (tick % 4) * 0.42,
                )

    for boundary in (10, 24, 40, 58, 80, 100, 118, 140, 154, 166):
        add_transition(mix, boundary - 0.42, 0.054 * energy_at(boundary))

    # A memorable two-bar hook supports comparison and the final human gate.
    hook = (74, 77, 81, 79, 77, 74, 72, 69)
    for hook_start in (102.0, 142.0):
        for index, note in enumerate(hook):
            add_pluck(
                mix,
                hook_start + index * BEAT / 2,
                note + 12,
                0.040 * energy_at(hook_start),
                -0.45 + (index % 3) * 0.45,
            )

    # Soft saturation and a precise fade make the generated file delivery-safe.
    mix = np.tanh(mix * 1.16)
    fade_in = min(sample_count, int(1.8 * SAMPLE_RATE))
    fade_out = min(sample_count, int(5.0 * SAMPLE_RATE))
    mix[:fade_in] *= np.linspace(0.0, 1.0, fade_in, dtype=np.float32)[:, None]
    mix[-fade_out:] *= np.linspace(1.0, 0.0, fade_out, dtype=np.float32)[:, None]
    peak = float(np.max(np.abs(mix)))
    if peak > 0:
        mix *= 0.88 / peak
    return mix


def write_pcm24(path: Path, audio: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    values = np.clip(audio, -1.0, 1.0)
    integers = (values * 8_388_607.0).astype(np.int32).reshape(-1)
    packed = np.empty((len(integers), 3), dtype=np.uint8)
    packed[:, 0] = integers & 0xFF
    packed[:, 1] = (integers >> 8) & 0xFF
    packed[:, 2] = (integers >> 16) & 0xFF
    with wave.open(str(path), "wb") as output:
        output.setnchannels(2)
        output.setsampwidth(3)
        output.setframerate(SAMPLE_RATE)
        output.writeframes(packed.tobytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--duration", type=float, default=174.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("media-source/pyroscan-tech-bed-v2-musical.wav"),
    )
    args = parser.parse_args()
    if args.duration <= 0:
        raise SystemExit("duration must be positive")

    audio = render(args.duration)
    write_pcm24(args.output, audio)
    print(
        f"Wrote original musical technology bed: {args.output} "
        f"({args.duration:.3f}s, {BPM:.0f} BPM, D minor, deterministic seed {RNG_SEED})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
