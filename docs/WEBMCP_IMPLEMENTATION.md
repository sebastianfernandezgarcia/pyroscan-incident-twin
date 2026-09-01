# WebMCP implementation

PyroScan uses the imperative WebMCP API from the top-level page. The complete, searchable implementation lives in [`src/webmcp/registerIncidentTools.ts`](../src/webmcp/registerIncidentTools.ts).

## Registration and lifecycle

`src/main.tsx` starts one registration lifecycle before rendering the app. All six calls use:

```ts
await document.modelContext.registerTool(tool, { signal: controller.signal })
```

The controller is aborted on `pagehide`, which unregisters the tools with the page. Browsers without WebMCP still receive the full human interface.

The code also tolerates current hosts that omit the execution callback's optional cancellation signal, while honoring it whenever supplied.

## One shared state

The React UI and every tool call the same actions in `src/store/incidentStore.ts`. There is no duplicate tool-only data layer.

```text
human control ─┐
               ├─> incidentStore action ─> map / cards / activity / result
WebMCP tool ───┘
```

This makes collaboration bidirectional:

1. A human adds a blocked road.
2. `read_incident_board` returns it to the agent.
3. Later comparison scores account for the route constraint.
4. A staged plan names that exact constraint in its access action.
5. If knowledge changes after staging, the plan becomes `needs-review`.

## Tool contracts

### `read_incident_board`

- Empty, strict object input.
- Returns a compact board snapshot, not the full UI state.
- Returns separately labeled `publicContext` for EMSR671, SITCAN terrain and the OSM coastline, including source URLs and `drivesSimulation: false`.
- Includes the exact `boardVersion` needed for staging.
- `readOnlyHint: true` and `untrustedContentHint: true` because human notes may be present.

### `inspect_zone`

- `zoneId`: one of four explicit exercise sectors.
- Focuses that sector visibly and returns bounded evidence split into public context and synthetic fixtures.
- Treated as read-only because it changes only visual selection.

### `simulate_spread`

- `horizonMinutes`: `30 | 60 | 90`.
- `windPreset`: `observed | northeast-shift | gusting-west`.
- Replaces the active scenario, increments `boardVersion` and clears unapproved drafts.
- Output calls the result an exercise attention area, never a forecast.

### `compare_response_options`

- Takes two or three unique IDs from a closed set.
- Scores only against the current scenario and annotations.
- Does not stage or approve anything.

### `stage_response_plan`

- Requires `boardVersion`, `scenarioId`, `optionId` and a short rationale.
- Rejects stale versions with a recoverable `[STALE_BOARD]` error.
- Opens a visible, reversible draft.
- Cannot approve a plan.

### `add_board_annotation`

- Takes a bounded type, zone and 1–280 character note.
- Makes the note visible on map/evidence surfaces.
- Marks any existing staged plan `needs-review`.
- Uses `untrustedContentHint: true`.

Every schema uses `additionalProperties: false`, and the execute callback repeats strict runtime validation rather than trusting schema enforcement alone.

## Public context boundary

The shared store exposes public-data provenance to both people and agents without conflating it with the active model:

- Copernicus EMSR671: historical 2023 observed burn-scar reference;
- SITCAN/GRAFCAN: 25 m terrain context;
- OpenStreetMap: La Palma coastline;
- synthetic fixtures: ignition, wind, access graph, attention contours, risk and response scores.

`read_incident_board` returns `drivesSimulation: false` and a plain-language separation rule with every public context bundle. Full hashes and derivation details are in [`PUBLIC_DATA_PROVENANCE.md`](PUBLIC_DATA_PROVENANCE.md).

## State lineage

`boardVersion` is monotonic. Simulations, comparisons, annotations, staging, approval and undo all create a new version. Undo restores content but never restores the old version number; otherwise an earlier stale proposal could accidentally become valid again.

## Human authority

Plan approval is a React action and is not registered with WebMCP. This is visible in the decision workbench and asserted in the WebMCP test suite.

## Verification

`src/webmcp/registerIncidentTools.test.ts` verifies:

- the six exact tools are registered;
- no approval tool exists;
- one AbortSignal controls the lifecycle;
- agent calls mutate the same visual state;
- stale staging is rejected;
- callback options remain compatible with current hosts.
- public context remains explicitly non-live and separate from the synthetic active scenario.

The full journey has also been executed through the ChatGPT/Codex in-app browser's WebMCP capability, not only by direct unit calls.
