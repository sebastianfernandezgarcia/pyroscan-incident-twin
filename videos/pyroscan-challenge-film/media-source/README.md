# PyroScan original music bed

`pyroscan-tech-bed-original.wav` is a deterministic, original 174-second
ambient technology bed generated entirely from oscillators, envelopes, and
filtered pink noise defined in `../scripts/generate_tech_bed.py`.

It contains no samples, vocals, third-party composition, or licensed catalog
material. The WAV is intentionally ignored because it is reproducible and is
about 48 MB.

Regenerate and register it locally:

```bash
./scripts/generate_tech_bed.py \
  --duration 174 \
  --output media-source/pyroscan-tech-bed-original.wav

node ~/.agents/skills/media-use/scripts/resolve.mjs \
  --type bgm \
  --intent "Original deterministic PyroScan ambient technology bed" \
  --from media-source/pyroscan-tech-bed-original.wav \
  --project .
```

The final voice/music mix is created by `../scripts/assemble_voiceover.py`.
It targets the music at −26 LUFS before the narration sidechain and caps the
finished programme at −1.5 dBTP.
