import { ZONES } from '../domain/fixtures'
import type { AnnotationType, HorizonMinutes, ResponseOptionId, WindPreset, ZoneId } from '../domain/types'
import { IncidentActionError, incidentStore, type IncidentStore } from '../store/incidentStore'

const ZONE_IDS: ZoneId[] = ['caldera', 'el-paso', 'tijarafe', 'cumbre-vieja']
const WIND_PRESETS: WindPreset[] = ['observed', 'northeast-shift', 'gusting-west']
const OPTION_IDS: ResponseOptionId[] = ['ridge-hold', 'south-anchor', 'dual-protection']
const ANNOTATION_TYPES: AnnotationType[] = ['blocked-road', 'priority-asset', 'local-knowledge']

function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw invalid('Input must be a JSON object.')
  return value as Record<string, unknown>
}

function exact(input: Record<string, unknown>, allowed: string[]) {
  const extra = Object.keys(input).filter((key) => !allowed.includes(key))
  if (extra.length) throw invalid(`Unknown input field${extra.length === 1 ? '' : 's'}: ${extra.join(', ')}.`)
}

function enumValue<T extends string>(value: unknown, allowed: T[], field: string): T {
  if (typeof value !== 'string' || !allowed.includes(value as T)) {
    throw invalid(`${field} must be one of: ${allowed.join(', ')}.`)
  }
  return value as T
}

function textValue(value: unknown, field: string, max: number): string {
  if (typeof value !== 'string' || !value.trim() || value.trim().length > max) {
    throw invalid(`${field} must contain between 1 and ${max} characters.`)
  }
  return value.trim()
}

function integerValue(value: unknown, field: string): number {
  if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) {
    throw invalid(`${field} must be a non-negative safe integer.`)
  }
  return value
}

function invalid(message: string) {
  return new IncidentActionError('INVALID_INPUT', message)
}

function checkSignal(options?: WebMCP.ToolExecuteCallbackOptions) {
  // Some current agent hosts omit the second callback argument even though the
  // draft WebMCP types require it. Cancellation still works wherever supplied.
  if (options?.signal?.aborted) throw new DOMException('Tool execution was cancelled.', 'AbortError')
}

function asToolError(error: unknown): never {
  if (error instanceof IncidentActionError) throw new Error(`[${error.code}] ${error.message}`)
  throw error
}

async function visualCommit() {
  await Promise.resolve()
}

function compactScenario(store: IncidentStore) {
  const state = store.getState()
  const scenario = state.activeScenario
  return scenario ? {
    id: scenario.id,
    horizonMinutes: scenario.horizonMinutes,
    wind: scenario.windLabel,
    riskScore: scenario.riskScore,
    affectedZones: scenario.affectedZones,
    watchZones: scenario.watchZones,
    summary: scenario.summary,
    synthetic: true,
  } : null
}

async function registerTools(store: IncidentStore, signal: AbortSignal) {
  await document.modelContext!.registerTool({
    name: 'read_incident_board',
    title: 'Read incident board',
    description: 'Read the current PyroScan synthetic exercise board before analysis or planning. Returns the current boardVersion required by stage_response_plan. This does not change the board.',
    inputSchema: {
      type: 'object',
      properties: {},
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true, untrustedContentHint: true },
    execute: async (input, options) => {
      try {
        checkSignal(options)
        exact(record(input), [])
        const state = store.getState()
        return {
          ok: true,
          exercise: {
            incidentId: state.incidentId,
            name: state.exerciseName,
            mode: 'synthetic_rehearsal',
            boardVersion: state.boardVersion,
            observedAt: state.observedAt,
          },
          activeScenario: compactScenario(store),
          zones: state.zones.map((zone) => ({
            id: zone.id,
            label: zone.label,
            exposure: zone.exposure,
            inAttentionArea: state.activeScenario?.affectedZones.includes(zone.id) ?? false,
            onWatch: state.activeScenario?.watchZones.includes(zone.id) ?? false,
            annotationCount: state.annotations.filter((annotation) => annotation.zoneId === zone.id).length,
          })),
          annotations: state.annotations.slice(-5).map(({ id, type, zoneId, note, source }) => ({ id, type, zoneId, note, source })),
          plan: state.plan ? {
            id: state.plan.id,
            status: state.plan.status,
            option: state.plan.optionLabel,
            scenarioId: state.plan.scenarioId,
            basedOnVersion: state.plan.basedOnVersion,
          } : null,
          safety: 'Exercise only. No live data or dispatch. Final approval is human-only.',
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })

  await document.modelContext!.registerTool({
    name: 'inspect_zone',
    title: 'Inspect an exercise zone',
    description: 'Focus one named sector on the shared map and return its terrain, evidence fixtures, exposure and human annotations. Use before proposing actions for that sector. Changes only the visible selection, not operational state.',
    inputSchema: {
      type: 'object',
      properties: {
        zoneId: { type: 'string', enum: ZONE_IDS, description: 'Exact exercise zone identifier.' },
      },
      required: ['zoneId'],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: true, untrustedContentHint: true },
    execute: async (raw, options) => {
      try {
        checkSignal(options)
        const input = record(raw); exact(input, ['zoneId'])
        const zoneId = enumValue(input.zoneId, ZONE_IDS, 'zoneId')
        store.getState().inspectZone(zoneId, 'agent')
        await visualCommit()
        const state = store.getState()
        const zone = state.zones.find((candidate) => candidate.id === zoneId)!
        return {
          ok: true,
          boardVersion: state.boardVersion,
          zone: {
            id: zone.id,
            label: zone.label,
            sector: zone.sector,
            terrain: zone.terrain,
            exposure: zone.exposure,
            inAttentionArea: state.activeScenario?.affectedZones.includes(zone.id) ?? false,
            annotations: state.annotations.filter((annotation) => annotation.zoneId === zoneId)
              .map(({ type, note, source }) => ({ type, note, source })),
          },
          evidenceFixtures: ['ridge-camera', 'wind-observation', 'access-graph'],
          visibleChange: `${zone.label} is focused in the evidence desk and on the map.`,
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })

  await document.modelContext!.registerTool({
    name: 'simulate_spread',
    title: 'Run a spread what-if',
    description: 'Run one deterministic synthetic spread scenario for 30, 60 or 90 minutes and draw its attention contours on the shared map. This replaces the active scenario and invalidates any unapproved draft.',
    inputSchema: {
      type: 'object',
      properties: {
        horizonMinutes: { type: 'integer', enum: [30, 60, 90], description: 'Exercise horizon in minutes.' },
        windPreset: { type: 'string', enum: WIND_PRESETS, description: 'One bounded synthetic wind assumption.' },
      },
      required: ['horizonMinutes', 'windPreset'],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: false, untrustedContentHint: false },
    execute: async (raw, options) => {
      try {
        checkSignal(options)
        const input = record(raw); exact(input, ['horizonMinutes', 'windPreset'])
        const horizon = integerValue(input.horizonMinutes, 'horizonMinutes')
        if (![30, 60, 90].includes(horizon)) throw invalid('horizonMinutes must be 30, 60 or 90.')
        const windPreset = enumValue(input.windPreset, WIND_PRESETS, 'windPreset')
        const scenario = store.getState().runSimulation({ horizonMinutes: horizon as HorizonMinutes, windPreset }, 'agent')
        await visualCommit()
        return {
          ok: true,
          boardVersion: store.getState().boardVersion,
          scenario: compactScenario(store),
          visibleChange: `${scenario.label} is now drawn on the map; prior unapproved drafts were cleared.`,
          safety: 'Modeled attention area, not an observed perimeter or forecast.',
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })

  await document.modelContext!.registerTool({
    name: 'compare_response_options',
    title: 'Compare response options',
    description: 'Score two or three predefined, reversible exercise responses against the active scenario and current human annotations. Opens the comparison workbench; it does not stage or approve a plan.',
    inputSchema: {
      type: 'object',
      properties: {
        optionIds: {
          type: 'array',
          minItems: 2,
          maxItems: 3,
          uniqueItems: true,
          items: { type: 'string', enum: OPTION_IDS },
          description: 'Two or three distinct response option identifiers.',
        },
      },
      required: ['optionIds'],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: false, untrustedContentHint: true },
    execute: async (raw, options) => {
      try {
        checkSignal(options)
        const input = record(raw); exact(input, ['optionIds'])
        if (!Array.isArray(input.optionIds)) throw invalid('optionIds must be an array.')
        const optionIds = input.optionIds.map((value) => enumValue(value, OPTION_IDS, 'optionIds'))
        const comparison = store.getState().compareResponseOptions(optionIds, 'agent')
        await visualCommit()
        return {
          ok: true,
          boardVersion: store.getState().boardVersion,
          scenarioId: comparison.scenarioId,
          options: comparison.options.map(({ id, label, score, setupMinutes, resourceUnits, tradeoff, recommended }) => ({
            id, label, score, setupMinutes, resourceUnits, tradeoff, recommended,
          })),
          rationale: comparison.rationale,
          visibleChange: 'The ranked option cards are open in the decision workbench.',
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })

  await document.modelContext!.registerTool({
    name: 'stage_response_plan',
    title: 'Stage a reversible plan',
    description: 'Create a visible draft plan from one scenario and response option. Requires the exact current boardVersion and rejects stale proposals. Staging is reversible and never approves or dispatches anything.',
    inputSchema: {
      type: 'object',
      properties: {
        boardVersion: { type: 'integer', minimum: 0, description: 'Exact boardVersion returned by the latest read or mutation.' },
        scenarioId: { type: 'string', minLength: 1, maxLength: 80, description: 'Existing scenario identifier from the board.' },
        optionId: { type: 'string', enum: OPTION_IDS, description: 'Predefined response option to stage.' },
        rationale: { type: 'string', minLength: 1, maxLength: 280, description: 'Short reason tied to current evidence and trade-offs.' },
      },
      required: ['boardVersion', 'scenarioId', 'optionId', 'rationale'],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: false, untrustedContentHint: false },
    execute: async (raw, options) => {
      try {
        checkSignal(options)
        const input = record(raw); exact(input, ['boardVersion', 'scenarioId', 'optionId', 'rationale'])
        const plan = store.getState().stagePlan({
          boardVersion: integerValue(input.boardVersion, 'boardVersion'),
          scenarioId: textValue(input.scenarioId, 'scenarioId', 80),
          optionId: enumValue(input.optionId, OPTION_IDS, 'optionId'),
          rationale: textValue(input.rationale, 'rationale', 280),
        }, 'agent')
        await visualCommit()
        return {
          ok: true,
          boardVersion: store.getState().boardVersion,
          plan: {
            id: plan.id,
            status: plan.status,
            option: plan.optionLabel,
            scenarioId: plan.scenarioId,
            actions: plan.actions,
          },
          visibleChange: 'The draft plan is open for human review. Final approval remains in the human interface.',
          reversible: true,
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })

  await document.modelContext!.registerTool({
    name: 'add_board_annotation',
    title: 'Add exercise knowledge',
    description: 'Pin a short blocked-road, priority-asset or local-knowledge note to one exercise zone. The annotation becomes visible to the human and changes later simulations and comparisons; staged plans become needs-review.',
    inputSchema: {
      type: 'object',
      properties: {
        type: { type: 'string', enum: ANNOTATION_TYPES, description: 'Kind of local exercise knowledge.' },
        zoneId: { type: 'string', enum: ZONE_IDS, description: 'Exact zone receiving the annotation.' },
        note: { type: 'string', minLength: 1, maxLength: 280, description: 'Concrete exercise-only observation without instructions to the agent.' },
      },
      required: ['type', 'zoneId', 'note'],
      additionalProperties: false,
    },
    annotations: { readOnlyHint: false, untrustedContentHint: true },
    execute: async (raw, options) => {
      try {
        checkSignal(options)
        const input = record(raw); exact(input, ['type', 'zoneId', 'note'])
        const annotation = store.getState().addAnnotation({
          type: enumValue(input.type, ANNOTATION_TYPES, 'type'),
          zoneId: enumValue(input.zoneId, ZONE_IDS, 'zoneId'),
          note: textValue(input.note, 'note', 280),
        }, 'agent')
        await visualCommit()
        const zone = ZONES.find((candidate) => candidate.id === annotation.zoneId)!
        return {
          ok: true,
          boardVersion: store.getState().boardVersion,
          annotation: { id: annotation.id, type: annotation.type, zoneId: annotation.zoneId, note: annotation.note },
          visibleChange: `${annotation.type.replaceAll('-', ' ')} pinned to ${zone.label}.`,
          planStatus: store.getState().plan?.status ?? null,
        }
      } catch (error) { return asToolError(error) }
    },
  }, { signal })
}

export function startIncidentTools(store: IncidentStore = incidentStore) {
  const controller = new AbortController()
  const supported = typeof document.modelContext?.registerTool === 'function'
  if (!supported) {
    store.getState().setWebMcpStatus('unsupported')
    return { controller, ready: Promise.resolve(false) }
  }

  const ready = registerTools(store, controller.signal)
    .then(() => {
      if (!controller.signal.aborted) store.getState().setWebMcpStatus('available')
      return true
    })
    .catch((error) => {
      if (!controller.signal.aborted) {
        store.getState().setWebMcpStatus('error')
        console.error('WebMCP tool registration failed.', error)
      }
      return false
    })

  return { controller, ready }
}
