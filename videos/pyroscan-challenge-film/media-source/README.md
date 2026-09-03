# PyroScan original music bed

`pyroscan-tech-bed-v2-musical.wav` is a deterministic, original 174-second
musical technology bed generated entirely from synthesis defined in
`../scripts/generate_tech_bed.py`.

The approved musical direction replaces the original amorphous drone with a clear 104 BPM
pulse, glassy arpeggios, bass, restrained synthetic percussion, transition
motifs and scene-aware energy. It remains deliberately quiet under narration.

It contains no samples, vocals, third-party composition, or licensed catalog
material. The WAV is intentionally ignored because it is reproducible and is
about 48 MB. Generation requires Python 3 and NumPy.

Regenerate and register it locally:

```bash
./scripts/generate_tech_bed.py \
  --duration 174 \
  --output media-source/pyroscan-tech-bed-v2-musical.wav

node ~/.agents/skills/media-use/scripts/resolve.mjs \
  --type bgm \
  --intent "Original animated musical PyroScan technology bed" \
  --from media-source/pyroscan-tech-bed-v2-musical.wav \
  --project .
```

The final voice/music mix is created by `../scripts/assemble_voiceover.py`.
It targets the music at −26 LUFS before the narration sidechain and caps the
finished programme at −1.5 dBTP.
