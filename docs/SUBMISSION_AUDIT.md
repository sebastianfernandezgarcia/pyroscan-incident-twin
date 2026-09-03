# WebMCP Challenge submission audit

**Verdict:** **SUBMITTED.** PyroScan is technically eligible, the runnable product is public on two origins, the narrated 2:54 demo is publicly embedded from YouTube, and Devpost confirms the project is submitted to The WebMCP Challenge.

Audit date: **3 September 2026**

Deadline: **3 September 2026, 1:00 PM PDT / 9:00 PM Atlantic/Canary**

## Required submission items

| Official requirement | Status | Evidence / next action |
| --- | --- | --- |
| WebMCP-powered web app | **PASS** | Six imperative tools share the same Zustand store as the visible UI. See [`src/webmcp/registerIncidentTools.ts`](../src/webmcp/registerIncidentTools.ts). |
| Working live URL | **PASS** | [Primary Netlify deployment](https://pyroscan-incident-twin.netlify.app/) and [GitHub Pages mirror](https://sebastianfernandezgarcia.github.io/pyroscan-incident-twin/) load without authentication. |
| Runs in a supported judge environment | **PASS** | Verified in the ChatGPT/Codex built-in browser with GPT-5.6 Sol; all six Site Tools were discovered and invoked. |
| Complete, coherent product | **PASS** | Responsive three-pane workbench, shared state, deterministic simulator, comparison, reversible plan, activity log, undo and reset. |
| English description covers fit, UX, collaboration and implementation | **PASS** | Final copy is in [`DEVPOST_SUBMISSION.md`](DEVPOST_SUBMISSION.md). |
| Public source repository | **PASS** | [Public GitHub repository](https://github.com/sebastianfernandezgarcia/pyroscan-incident-twin). |
| All code, assets and instructions included | **PASS** | Clean clone requires only `npm install`, `npm test`, and `npm run build`; no backend, API key or private dataset. |
| Open-source license visible | **PASS** | MIT license at repository root and detected in the GitHub About area. |
| Pre-existing work documented | **PASS** | [`CHALLENGE_WORK.md`](../CHALLENGE_WORK.md) separates prior private PyroScan research from the new competition implementation and commit history. |
| Video under three minutes, with audio and clear WebMCP demo | **PASS** | The [public YouTube demo](https://youtu.be/wIsJsnfs2EI) is 2:54, processed at 2160p 4K, contains audible English narration and a quiet original bed at −16.3 LUFS / −1.5 dBTP, and shows the complete WebMCP journey. See [`FINAL_VIDEO_RECEIPT.md`](FINAL_VIDEO_RECEIPT.md). |
| Submission materials in English | **PASS** | App, repository, description, testing instructions, captions and narration are English. |
| No unauthorized marks, music or media | **PASS** | Original interface and animation. The technology bed is generated from authored synthesis with no samples, vocals or third-party music. OpenStreetMap, Copernicus EMSR671 and SITCAN/GRAFCAN public-data attributions are visible/source-linked and documented. |
| Devpost form completed before deadline | **PASS** | Devpost showed **Project submitted!** and the public page shows **Submitted to — The WebMCP Challenge**: [PyroScan // Incident Twin](https://devpost.com/software/pyroscan-incident-twin). |

Official source of truth: [WebMCP Challenge rules](https://webmcp.devpost.com/rules).

## Judge-criteria evidence

| Criterion | What the judge should see in the first 90 seconds |
| --- | --- |
| **WebMCP Leverage** | Intent-level tools, not click wrappers; human annotations affect later agent analysis; all effects appear on the same live map; exact `boardVersion` rejects stale proposals. |
| **Execution** | A polished responsive product, real La Palma coastline, public 25 m terrain, an observed 2023 Copernicus burn-scar reference, deterministic offline demo, six working tools, tests, visible activity lineage, reversible draft and human-only approval. |
| **Potential Impact** | A credible rehearsal workflow for exercise facilitators, local operators and civil-protection training teams who must test trade-offs before a live crisis. |
| **Creativity & Ambition** | A browser becomes a shared incident twin where agent exploration and human judgment complement each other instead of replacing one another. |

## Claims policy

Use these phrases:

- **wildfire readiness and rehearsal**;
- **synthetic, deterministic exercise scenario**;
- **grounded in public La Palma terrain and historical Copernicus evidence**;
- **public context is historical/geographic and does not drive the simulator**;
- **explores decision trade-offs before a live incident**;
- **working, open-source WebMCP prototype**.

Do **not** claim that the competition build:

- is deployed by Canary Islands emergency services;
- has prevented a real fire or evacuation;
- predicts real wildfire spread;
- consumes live sensor, weather or incident data;
- dispatches resources or sends public alerts.

Those claims require public, verifiable evidence and capabilities that are intentionally outside this build.

## Final freeze gate

After the submission period ends, do not change the judged website, repository or submission. Before the deadline:

- [x] Confirm the public YouTube video is under 3:00 and audible.
- [x] Confirm public 2160p playback and a retrievable manual English caption track.
- [x] Run the exact judge journey against the submitted live URL.
- [x] Confirm Site Tools shows six tools.
- [x] Open the repository without repository credentials and verify public access and MIT license visibility.
- [x] Review every Devpost field, technology tag, gallery item, embedded video and link.
- [x] Submit before 9:00 PM Canary Islands, leaving a safety margin.
- [x] Preserve a local copy of the submitted text, images and video URL.

See [`SUBMISSION_RECEIPT.md`](SUBMISSION_RECEIPT.md) for the final public links and validation signals.
