# Devpost submission copy

**Paste-ready:** all public text is in English. PyroScan should be entered as an **Existing project, meaningfully extended during the challenge** so the prior research context and new WebMCP build are transparent.

## Project name

**PyroScan // Incident Twin**

## Elevator pitch — 179 / 200 characters

**Wildfire readiness, rehearsed together: people add local knowledge while AI agents inspect evidence, run bounded what-ifs, compare responses and stage a safe plan on one live map.**

## One-line summary

PyroScan lets a human exercise director and ChatGPT inspect evidence, run synthetic wildfire what-ifs, compare reversible response options and prepare a briefing on the same live map through WebMCP.

## Inspiration

Wildfire readiness needs a rehearsal space before the crisis. Exercises combine sensor evidence, local knowledge, changing assumptions and high-consequence decisions. Traditional dashboards are built for human clicks, while chat assistants reason in a separate window and quickly lose the state visible on the map. We wanted a safer collaboration model: an agent can help inspect and compare, but the human keeps context, authority and the final decision.

La Palma is the visual setting because its steep terrain, interfaces and limited access make the value of a shared spatial artifact immediately understandable. The product is grounded in public terrain and a historical observed burn scar, while the active incident, wind, spread, risk and response scenario remain explicitly synthetic.

## What it does

PyroScan Incident Twin opens a deterministic wildfire exercise board with four sectors, the real outline of La Palma, a public 25 m SITCAN/GRAFCAN terrain hillshade, the corrected Copernicus EMSR671 burn scar from the July 2023 wildfire, animated synthetic fire/smoke/spread cues, modeled attention contours, local annotations, response options and an activity record.

Through six WebMCP site tools, ChatGPT can:

- read the compact current board with separately labeled public-data provenance;
- focus one exercise sector;
- run a 30, 60 or 90-minute bounded wind what-if;
- compare two or three predefined reversible response options;
- add a local route, asset or knowledge annotation;
- stage a visible response plan for review.

Every agent action changes the same interface the human sees. Human annotations affect later scores and appear in the staged plan. A monotonic board version rejects stale proposals. Final approval is deliberately not exposed as a tool and remains in the human interface.

## How we built it

The app is a static React 19, TypeScript and Vite application with no backend or API key. A Zustand vanilla store is the shared source of truth for React controls and WebMCP execute callbacks. The incident map is custom SVG with three locally bundled public layers: a simplified OpenStreetMap coastline, a hillshade derived from the SITCAN/GRAFCAN 25 m terrain model, and a projected Copernicus EMSR671 corrected burn-scar geometry. The critical demo therefore has no runtime tile or network dependency. A motion system renders synthetic fire, smoke, embers, wind vectors, scan passes and animated attention contours. The scenario engine is deterministic and uses a small set of synthetic fixtures.

Public context is a first-class part of the WebMCP contract: `read_incident_board` returns each source, observation date and role with `drivesSimulation: false`. The interface uses a separate blue historical layer, while the active what-if remains orange and explicitly synthetic. Exact source products, hashes, update dates and derivation steps are committed in `docs/PUBLIC_DATA_PROVENANCE.md`.

The six tools are registered imperatively with `document.modelContext.registerTool` in the top-level page. Inputs use strict JSON Schemas with `additionalProperties: false`, plus independent runtime validation. Read-only and untrusted-content hints describe behavior. One AbortController owns the registration lifecycle. Tests verify registration, shared-state mutations, stale-state rejection, human-only approval and compatibility with current browser callback behavior.

## Why WebMCP

Without WebMCP, an agent must infer a complex spatial workflow from labels and pixels or reproduce the whole application inside chat. With WebMCP, the website exposes domain intent — `inspect_zone`, `simulate_spread`, `compare_response_options` — while preserving the normal visual product, current session and human control.

This creates a loop that was previously awkward: the person adds local knowledge on the map; the agent reads it, explores alternatives and stages a structured artifact; the person sees exactly what changed and chooses whether to approve. The value comes from sharing state and complementary roles, not from automating more clicks.

## Challenges

- Designing tools that express domain intent without exposing unsafe emergency actions.
- Keeping every agent-driven state change synchronized with all human controls.
- Preventing a plausible proposal from silently surviving after the human changes evidence.
- Making synthetic provenance impossible to miss while still delivering a visually compelling demo.
- Integrating authentic public evidence without implying that historical observations are live inputs or forecasts.
- Supporting an experimental browser API whose runtime callback behavior is slightly looser than its current TypeScript definitions.

## Accomplishments

- A complete human-and-agent collaboration loop on one visual artifact.
- Deterministic, browser-only execution with no fragile external dependency.
- Runtime-tested Site Tools discovered and invoked in the ChatGPT/Codex built-in browser.
- Monotonic state lineage, reversible drafts, undo and human-only approval.
- A polished responsive workbench and open-source test suite.
- A geographically authentic La Palma surface with 25 m public terrain, a real historical Copernicus burn scar and cinematic but restrained exercise motion.

## What we learned

The strongest WebMCP tools are not wrappers around buttons. They expose a product's real verbs and make side effects visible. We also learned that undo must create a new version rather than restore an old version; otherwise a stale proposal can accidentally become valid again. Finally, human input should visibly change the downstream artifact, not merely influence an invisible score.

## What's next

The competition build intentionally keeps the active scenario synthetic and browser-only. A future research version could connect authorized live or exercise datasets, introduce facilitator-authored scenarios, compare team decisions across rehearsals and export after-action reports — while keeping the same human authority, provenance and stale-state safeguards.

## Built with

`WebMCP` `React` `TypeScript` `Vite` `Zustand` `SVG` `Vitest` `ChatGPT` `Codex`

## Links

- Live app (primary): `https://pyroscan-incident-twin.netlify.app/`
- Live app (GitHub Pages mirror): `https://sebastianfernandezgarcia.github.io/pyroscan-incident-twin/`
- Public repository: `https://github.com/sebastianfernandezgarcia/pyroscan-incident-twin`
- YouTube demo (<3 minutes): `https://youtu.be/5LNXxK6tD9Q`

## Additional information — exact answers

| Field | Answer |
| --- | --- |
| Submitter type | **Individual** |
| Country | **Spain** |
| Organization | Leave blank |
| App status | **Existing** |
| Significant WebMCP extension | **PyroScan previously existed as a broader private research concept. During the challenge period I created this separate, public browser-only product: a deterministic synthetic exercise engine, a shared human/agent incident board, six imperative WebMCP tools, exact state-lineage safeguards, locally derived public La Palma terrain and Copernicus historical wildfire context, automated tests and complete open-source documentation. CHALLENGE_WORK.md and the public commit history distinguish all new competition work.** |
| Live URL | `https://pyroscan-incident-twin.netlify.app/` |
| Public repo | `https://github.com/sebastianfernandezgarcia/pyroscan-incident-twin` |
| Agent/client tested | **ChatGPT/Codex built-in browser with GPT-5.6 Sol; automated registration and integration tests.** |
| AI tools leveraged | **OpenAI Codex desktop app, GPT-5.6 Sol, ChatGPT Site Tools / WebMCP, HyperFrames, and ElevenLabs for the English voiceover.** |
| Learning level | **Significant** |
| Gained career AI value | **Yes** |

## Testing instructions

Open the live URL in the latest ChatGPT desktop app's built-in browser using GPT-5.6 Sol or GPT-5.6 Terra. Select **Site tools** in the address bar; PyroScan should expose six tools. No login or API key is required.

Ask:

> Inspect El Paso. Add a blocked-road exercise note for the LP-3 checkpoint. Simulate a 60-minute northeast wind shift, compare the ridge and dual-interface options, then stage the safest reversible plan.

Expected visible result: El Paso focuses; an amber route note appears; the attention contours and wind indicator move; comparison cards rerank; and a reversible draft opens with the route constraint included. Final approval remains available only in the human interface.

If Site Tools are unavailable, confirm the current client/model supports WebMCP. The visual exercise still works manually, but the judged agent journey requires Site Tools.

## Gallery captions

1. [`docs/assets/gallery/01-shared-rehearsal-3x2.jpg`](assets/gallery/01-shared-rehearsal-3x2.jpg) — **One shared incident surface** — Public 25 m La Palma terrain and the Copernicus 2023 historical burn scar sit beside the clearly separate synthetic what-if and decision controls visible to both the human and the agent.
2. [`docs/assets/gallery/02-local-knowledge-3x2.jpg`](assets/gallery/02-local-knowledge-3x2.jpg) — **Local knowledge changes the result** — A route constraint added through WebMCP becomes visible on the board and affects later analysis.
3. [`docs/assets/gallery/03-webmcp-comparison-3x2.jpg`](assets/gallery/03-webmcp-comparison-3x2.jpg) — **Intent-level Site Tools** — Six WebMCP tools expose the domain verbs of the product instead of brittle sequences of clicks.
4. [`docs/assets/gallery/04-human-review-3x2.jpg`](assets/gallery/04-human-review-3x2.jpg) — **Human authority by design** — The agent can inspect, simulate, compare, annotate and stage; only the exercise director can approve.

Thumbnail: [`docs/assets/devpost-thumbnail-3x2.jpg`](assets/devpost-thumbnail-3x2.jpg)
