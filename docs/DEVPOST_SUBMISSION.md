# Devpost submission copy

All public submission text is in English as required.

## Project name

**PyroScan // Incident Twin**

## Tagline

**A shared wildfire rehearsal table for people and AI agents.**

## One-line summary

PyroScan lets a human exercise director and ChatGPT inspect evidence, run synthetic wildfire what-ifs, compare reversible response options and prepare a briefing on the same live map through WebMCP.

## Inspiration

Wildfire response exercises combine sensor evidence, local knowledge, changing assumptions and high-consequence decisions. Traditional dashboards are built for human clicks, while chat assistants reason in a separate window and quickly lose the state visible on the map. We wanted to explore a safer collaboration model: an agent can help inspect and compare, but the human keeps context, authority and the final decision.

La Palma is the visual setting because its steep terrain, interfaces and limited access make the value of a shared spatial artifact immediately understandable. The submitted scenario is entirely synthetic.

## What it does

PyroScan Incident Twin opens a deterministic wildfire exercise board with evidence fixtures, four sectors, a custom map, modeled attention contours, local annotations, response options and an activity record.

Through six WebMCP site tools, ChatGPT can:

- read the compact current board;
- focus one exercise sector;
- run a 30, 60 or 90-minute bounded wind what-if;
- compare two or three predefined reversible response options;
- add a local route, asset or knowledge annotation;
- stage a visible response plan for review.

Every agent action changes the same interface the human sees. Human annotations affect later scores and appear in the staged plan. A monotonic board version rejects stale proposals. Final approval is deliberately not exposed as a tool and remains in the human interface.

## How we built it

The app is a static React 19, TypeScript and Vite application with no backend or API key. A Zustand vanilla store is the shared source of truth for React controls and WebMCP execute callbacks. The incident map is custom SVG, so the critical demo has no tile or network dependency. The scenario engine is deterministic and uses a small set of synthetic fixtures.

The six tools are registered imperatively with `document.modelContext.registerTool` in the top-level page. Inputs use strict JSON Schemas with `additionalProperties: false`, plus independent runtime validation. Read-only and untrusted-content hints describe behavior. One AbortController owns the registration lifecycle. Tests verify registration, shared-state mutations, stale-state rejection, human-only approval and compatibility with current browser callback behavior.

## Why WebMCP

Without WebMCP, an agent must infer a complex spatial workflow from labels and pixels or reproduce the whole application inside chat. With WebMCP, the website exposes domain intent — `inspect_zone`, `simulate_spread`, `compare_response_options` — while preserving the normal visual product, current session and human control.

This creates a loop that was previously awkward: the person adds local knowledge on the map; the agent reads it, explores alternatives and stages a structured artifact; the person sees exactly what changed and chooses whether to approve. The value comes from sharing state and complementary roles, not from automating more clicks.

## Challenges

- Designing tools that express domain intent without exposing unsafe emergency actions.
- Keeping every agent-driven state change synchronized with all human controls.
- Preventing a plausible proposal from silently surviving after the human changes evidence.
- Making synthetic provenance impossible to miss while still delivering a visually compelling demo.
- Supporting an experimental browser API whose runtime callback behavior is slightly looser than its current TypeScript definitions.

## Accomplishments

- A complete human-and-agent collaboration loop on one visual artifact.
- Deterministic, browser-only execution with no fragile external dependency.
- Runtime-tested Site Tools discovered and invoked in the ChatGPT/Codex built-in browser.
- Monotonic state lineage, reversible drafts, undo and human-only approval.
- A polished responsive workbench and open-source test suite.

## What we learned

The strongest WebMCP tools are not wrappers around buttons. They expose a product's real verbs and make side effects visible. We also learned that undo must create a new version rather than restore an old version; otherwise a stale proposal can accidentally become valid again. Finally, human input should visibly change the downstream artifact, not merely influence an invisible score.

## What's next

The competition build intentionally stays synthetic and browser-only. A future research version could connect authorized exercise datasets, introduce facilitator-authored scenarios, compare team decisions across rehearsals and export after-action reports — while keeping the same human authority, provenance and stale-state safeguards.

## Built with

`WebMCP` `React` `TypeScript` `Vite` `Zustand` `SVG` `Vitest` `ChatGPT` `Codex`

## Links to add before submission

- Live app: `TODO`
- Public repository: `https://github.com/sebastianfernandezgarcia/pyroscan-incident-twin`
- YouTube demo (<3 minutes): `TODO`
