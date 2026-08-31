# WebMCP Challenge submission audit

**Verdict:** PyroScan is technically eligible and the runnable product is ready. The only hard blockers are the public narrated video and the final Devpost entry. Netlify is optional because the verified GitHub Pages URL already satisfies the hosting rule.

Audit date: **31 August 2026**  
Deadline: **3 September 2026, 1:00 PM PDT / 9:00 PM Atlantic/Canary**

## Required submission items

| Official requirement | Status | Evidence / next action |
| --- | --- | --- |
| WebMCP-powered web app | **PASS** | Six imperative tools share the same Zustand store as the visible UI. See [`src/webmcp/registerIncidentTools.ts`](../src/webmcp/registerIncidentTools.ts). |
| Working live URL | **PASS** | [GitHub Pages deployment](https://sebastianfernandezgarcia.github.io/pyroscan-incident-twin/) loads without authentication. |
| Runs in a supported judge environment | **PASS** | Verified in the ChatGPT/Codex built-in browser with GPT-5.6 Sol; all six Site Tools were discovered and invoked. |
| Complete, coherent product | **PASS** | Responsive three-pane workbench, shared state, deterministic simulator, comparison, reversible plan, activity log, undo and reset. |
| English description covers fit, UX, collaboration and implementation | **PASS** | Final copy is in [`DEVPOST_SUBMISSION.md`](DEVPOST_SUBMISSION.md). |
| Public source repository | **PASS** | [Public GitHub repository](https://github.com/sebastianfernandezgarcia/pyroscan-incident-twin). |
| All code, assets and instructions included | **PASS** | Clean clone requires only `npm install`, `npm test`, and `npm run build`; no backend, API key or private dataset. |
| Open-source license visible | **PASS** | MIT license at repository root and detected in the GitHub About area. |
| Pre-existing work documented | **PASS** | [`CHALLENGE_WORK.md`](../CHALLENGE_WORK.md) separates prior private PyroScan research from the new competition implementation and commit history. |
| Video under three minutes, with audio and clear WebMCP demo | **BLOCKED** | The checked 2:48 motion-design visual master, timed human-voice script and captions are ready. Approve/render it, add the recorded English narration, upload publicly to YouTube, and paste its URL. |
| Submission materials in English | **PASS** | App, repository, description, testing instructions, captions and narration are English. |
| No unauthorized marks, music or media | **PASS** | Original interface and animation; no commercial music. OpenStreetMap coastline attribution is visible in-app and documented. |
| Devpost form completed before deadline | **BLOCKED** | Create and save a separate PyroScan draft, add the final YouTube URL, review, and submit. Do not alter the Roque Nights draft. |

Official source of truth: [WebMCP Challenge rules](https://webmcp.devpost.com/rules).

## Judge-criteria evidence

| Criterion | What the judge should see in the first 90 seconds |
| --- | --- |
| **WebMCP Leverage** | Intent-level tools, not click wrappers; human annotations affect later agent analysis; all effects appear on the same live map; exact `boardVersion` rejects stale proposals. |
| **Execution** | A polished responsive product, real La Palma coastline, deterministic offline demo, six working tools, tests, visible activity lineage, reversible draft and human-only approval. |
| **Potential Impact** | A credible rehearsal workflow for exercise facilitators, local operators and civil-protection training teams who must test trade-offs before a live crisis. |
| **Creativity & Ambition** | A browser becomes a shared incident twin where agent exploration and human judgment complement each other instead of replacing one another. |

## Claims policy

Use these phrases:

- **wildfire readiness and rehearsal**;
- **synthetic, deterministic exercise scenario**;
- **designed around La Palma's terrain and constrained access**;
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

- [ ] Confirm the public YouTube video is under 3:00 and audible.
- [ ] Run the exact judge prompt against the submitted live URL.
- [ ] Confirm Site Tools shows six tools.
- [ ] Open the repository in a signed-out browser and verify license visibility.
- [ ] Review every Devpost field and link.
- [ ] Submit before 9:00 PM Canary Islands, leaving a safety margin.
- [ ] Preserve a local copy of the submitted text, images and video URL.
