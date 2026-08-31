# Work created for the WebMCP Challenge

This repository documents the new work completed for the OpenAI WebMCP Challenge beginning on 25 August 2026.

## New challenge work

- A standalone React/Vite/TypeScript application designed for public open-source release.
- A deterministic, browser-only synthetic wildfire exercise domain.
- A shared Zustand state model used by both the human interface and agent tools.
- A custom SVG incident map and three-pane evidence/map/decision workbench.
- Six imperative WebMCP tools registered in the top-level document.
- Runtime validation, read-only/untrusted-content annotations and lifecycle cleanup.
- Monotonic `boardVersion` lineage and stale-plan rejection.
- Reversible plan staging, undo and an intentionally human-only approval gate.
- Unit, integration and interface tests.
- Challenge-specific README, implementation guide, submission copy and demo script.

## Prior context

PyroScan existed previously as a broader private research/product project. That history informed the problem choice and the importance of synthetic provenance and human validation. The code in this public repository is a separate competition implementation and does not require the private product, its backend, credentials, datasets or services.

## Evaluation boundary

Judges can evaluate everything in this repository independently:

```bash
npm install
npm test
npm run build
```

No proprietary service or private dataset is needed.
