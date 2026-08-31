import { createStore } from 'zustand/vanilla'
import { EXERCISE_CLOCK, RESPONSE_OPTIONS, ZONES } from '../domain/fixtures'
import { compareOptions, simulateSpread } from '../domain/simulator'
import type {
  ActivityEvent,
  Annotation,
  AnnotationType,
  Comparison,
  HorizonMinutes,
  IncidentSnapshot,
  ResponseOptionId,
  ResponsePlan,
  SpreadScenario,
  WindPreset,
  ZoneId,
} from '../domain/types'

type Actor = 'agent' | 'human' | 'system'

interface SimulationRequest {
  horizonMinutes: HorizonMinutes
  windPreset: WindPreset
}

interface AnnotationRequest {
  type: AnnotationType
  zoneId: ZoneId
  note: string
}

interface PlanRequest {
  boardVersion: number
  scenarioId: string
  optionId: ResponseOptionId
  rationale: string
}

interface IncidentState extends IncidentSnapshot {
  focusedZoneId: ZoneId | null
  activePanel: 'evidence' | 'compare' | 'plan'
  webMcpStatus: 'checking' | 'available' | 'unsupported' | 'error'
  activity: ActivityEvent[]
  history: IncidentSnapshot[]
  inspectZone: (zoneId: ZoneId, actor: Actor) => void
  runSimulation: (request: SimulationRequest, actor: Actor) => SpreadScenario
  compareResponseOptions: (optionIds: ResponseOptionId[], actor: Actor) => Comparison
  stagePlan: (request: PlanRequest, actor: 'agent' | 'human-demo') => ResponsePlan
  addAnnotation: (request: AnnotationRequest, actor: 'agent' | 'human') => Annotation
  approvePlan: () => void
  undoLastChange: () => void
  resetExercise: () => void
  setWebMcpStatus: (status: IncidentState['webMcpStatus']) => void
  readSnapshot: () => IncidentSnapshot
}

export class IncidentActionError extends Error {
  constructor(
    public readonly code: 'INVALID_INPUT' | 'STALE_BOARD' | 'NOT_FOUND' | 'INVALID_STATE',
    message: string,
  ) {
    super(message)
    this.name = 'IncidentActionError'
  }
}

const defaultScenario = simulateSpread({ horizonMinutes: 60, windPreset: 'observed', annotations: [] })
const defaultComparison = compareOptions(defaultScenario, ['ridge-hold', 'south-anchor', 'dual-protection'], [])

const initialActivity: ActivityEvent[] = [
  {
    id: 'event-4',
    at: '18:42',
    actor: 'system',
    title: 'Exercise board ready',
    detail: 'Synthetic fixtures loaded locally. No live emergency data.',
  },
  {
    id: 'event-3',
    at: '18:39',
    actor: 'human',
    title: 'Observation validated',
    detail: 'Training ignition marker kept as the shared reference point.',
  },
  {
    id: 'event-2',
    at: '18:34',
    actor: 'system',
    title: 'Wind fixture refreshed',
    detail: 'ENE 18 km/h · synthetic observation pack.',
  },
  {
    id: 'event-1',
    at: '18:28',
    actor: 'system',
    title: 'Scenario opened',
    detail: 'LP-EX-042 · La Palma multi-agency rehearsal.',
  },
]

function snapshot(state: IncidentState): IncidentSnapshot {
  return structuredClone({
    boardVersion: state.boardVersion,
    incidentId: state.incidentId,
    exerciseName: state.exerciseName,
    observedAt: state.observedAt,
    zones: state.zones,
    annotations: state.annotations,
    scenarios: state.scenarios,
    activeScenario: state.activeScenario,
    comparison: state.comparison,
    plan: state.plan,
  })
}

function event(actor: Actor, title: string, detail: string, sequence: number): ActivityEvent {
  return {
    id: `event-runtime-${sequence}`,
    at: `18:${String(42 + sequence).padStart(2, '0')}`,
    actor,
    title,
    detail,
  }
}

function initialData() {
  return {
    boardVersion: 12,
    incidentId: 'LP-EX-042',
    exerciseName: 'Ridge Wind Shift / La Palma',
    observedAt: EXERCISE_CLOCK,
    zones: ZONES,
    annotations: [] as Annotation[],
    scenarios: [defaultScenario],
    activeScenario: defaultScenario,
    comparison: defaultComparison,
    plan: null,
    focusedZoneId: null,
    activePanel: 'compare' as const,
    webMcpStatus: 'checking' as const,
    activity: initialActivity,
    history: [] as IncidentSnapshot[],
  }
}

function validateNote(note: string) {
  const normalized = note.trim()
  if (!normalized || normalized.length > 280) {
    throw new IncidentActionError('INVALID_INPUT', 'Note must contain between 1 and 280 characters.')
  }
  return normalized
}

function buildPlan(
  request: PlanRequest,
  scenario: SpreadScenario,
  annotations: Annotation[],
  stagedAtVersion: number,
  stagedBy: 'agent' | 'human-demo',
): ResponsePlan {
  const option = RESPONSE_OPTIONS.find((candidate) => candidate.id === request.optionId)
  if (!option) throw new IncidentActionError('NOT_FOUND', `Unknown response option: ${request.optionId}.`)
  const firstZone = scenario.affectedZones[0] ?? 'el-paso'
  const blockedZone = annotations.find((annotation) => annotation.type === 'blocked-road')?.zoneId
  const accessZone = blockedZone ?? firstZone
  const zoneLabel = ZONES.find((zone) => zone.id === accessZone)?.label ?? accessZone
  const accessDetail = blockedZone
    ? `Resolve the recorded route constraint in ${zoneLabel}.`
    : `Check the route into ${zoneLabel}.`

  return {
    id: `plan-${scenario.id}-${request.optionId}`,
    scenarioId: scenario.id,
    optionId: request.optionId,
    optionLabel: option.label,
    basedOnVersion: request.boardVersion,
    stagedAtVersion,
    status: 'staged',
    rationale: validateNote(request.rationale),
    stagedBy,
    actions: [
      { id: 'brief', time: 'T+00', title: 'Brief the exercise team', detail: `Confirm ${scenario.windLabel}.`, owner: 'Coordination' },
      { id: 'access', time: 'T+08', title: 'Validate access', detail: accessDetail, owner: 'Mobility lead' },
      { id: 'position', time: `T+${option.setupMinutes}`, title: option.label, detail: `Stage ${option.resourceUnits} exercise units; no real dispatch.`, owner: 'Field lead' },
      { id: 'review', time: `T+${scenario.horizonMinutes}`, title: 'Human decision gate', detail: 'Review evidence, annotations and changed assumptions.', owner: 'Exercise director' },
    ],
  }
}

export function createIncidentStore() {
  return createStore<IncidentState>((set, get) => ({
    ...initialData(),

    inspectZone: (zoneId, actor) => {
      const zone = get().zones.find((candidate) => candidate.id === zoneId)
      if (!zone) throw new IncidentActionError('NOT_FOUND', `Unknown zone: ${zoneId}.`)
      set((state) => ({
        focusedZoneId: zoneId,
        activePanel: 'evidence',
        activity: [event(actor, `Focused ${zone.label}`, `${zone.sector} evidence is now visible on the shared board.`, state.activity.length), ...state.activity],
      }))
    },

    runSimulation: (request, actor) => {
      if (![30, 60, 90].includes(request.horizonMinutes)) {
        throw new IncidentActionError('INVALID_INPUT', 'Horizon must be 30, 60 or 90 minutes.')
      }
      const state = get()
      const scenario = simulateSpread({ ...request, annotations: state.annotations })
      set((current) => ({
        boardVersion: current.boardVersion + 1,
        history: [...current.history.slice(-9), snapshot(current)],
        scenarios: [...current.scenarios.filter((item) => item.id !== scenario.id), scenario],
        activeScenario: scenario,
        comparison: null,
        plan: current.plan?.status === 'approved' ? current.plan : null,
        activePanel: 'compare',
        activity: [event(actor, `Simulated ${scenario.label}`, scenario.summary, current.activity.length), ...current.activity],
      }))
      return scenario
    },

    compareResponseOptions: (optionIds, actor) => {
      const uniqueIds = [...new Set(optionIds)]
      if (uniqueIds.length < 2 || uniqueIds.length > 3) {
        throw new IncidentActionError('INVALID_INPUT', 'Compare two or three distinct response options.')
      }
      const state = get()
      if (!state.activeScenario) throw new IncidentActionError('INVALID_STATE', 'Run a spread scenario first.')
      if (uniqueIds.some((id) => !RESPONSE_OPTIONS.some((option) => option.id === id))) {
        throw new IncidentActionError('NOT_FOUND', 'At least one response option is unknown.')
      }
      const comparison = compareOptions(state.activeScenario, uniqueIds, state.annotations)
      set((current) => ({
        boardVersion: current.boardVersion + 1,
        history: [...current.history.slice(-9), snapshot(current)],
        comparison,
        activePanel: 'compare',
        activity: [event(actor, 'Compared response options', comparison.rationale, current.activity.length), ...current.activity],
      }))
      return comparison
    },

    stagePlan: (request, actor) => {
      const state = get()
      if (request.boardVersion !== state.boardVersion) {
        throw new IncidentActionError(
          'STALE_BOARD',
          `Board changed: expected version ${request.boardVersion}, current version is ${state.boardVersion}. Read the board again before staging.`,
        )
      }
      const scenario = state.scenarios.find((item) => item.id === request.scenarioId)
      if (!scenario) throw new IncidentActionError('NOT_FOUND', `Unknown scenario: ${request.scenarioId}.`)
      const stagedAtVersion = state.boardVersion + 1
      const plan = buildPlan(request, scenario, state.annotations, stagedAtVersion, actor)
      set((current) => ({
        boardVersion: stagedAtVersion,
        history: [...current.history.slice(-9), snapshot(current)],
        plan,
        activePanel: 'plan',
        activity: [event(actor === 'agent' ? 'agent' : 'human', 'Staged a reversible plan', `${plan.optionLabel} awaits human approval.`, current.activity.length), ...current.activity],
      }))
      return plan
    },

    addAnnotation: (request, actor) => {
      const state = get()
      if (!state.zones.some((zone) => zone.id === request.zoneId)) {
        throw new IncidentActionError('NOT_FOUND', `Unknown zone: ${request.zoneId}.`)
      }
      const note = validateNote(request.note)
      const annotation: Annotation = {
        id: `annotation-${state.annotations.length + 1}`,
        type: request.type,
        zoneId: request.zoneId,
        note,
        source: actor,
        createdAt: EXERCISE_CLOCK,
      }
      set((current) => ({
        boardVersion: current.boardVersion + 1,
        history: [...current.history.slice(-9), snapshot(current)],
        annotations: [...current.annotations, annotation],
        focusedZoneId: request.zoneId,
        plan: current.plan?.status === 'staged' ? { ...current.plan, status: 'needs-review' } : current.plan,
        activePanel: 'evidence',
        activity: [event(actor, 'Added local board knowledge', `${request.type.replaceAll('-', ' ')} · ${note}`, current.activity.length), ...current.activity],
      }))
      return annotation
    },

    approvePlan: () => {
      const state = get()
      if (!state.plan || state.plan.status !== 'staged' || state.plan.stagedAtVersion !== state.boardVersion) {
        throw new IncidentActionError('INVALID_STATE', 'Only a current staged plan can be approved. Restage after any board change.')
      }
      set((current) => ({
        boardVersion: current.boardVersion + 1,
        history: [...current.history.slice(-9), snapshot(current)],
        plan: current.plan ? { ...current.plan, status: 'approved' } : null,
        activity: [event('human', 'Plan approved by exercise director', 'The decision gate was completed in the human interface.', current.activity.length), ...current.activity],
      }))
    },

    undoLastChange: () => {
      const state = get()
      const previous = state.history.at(-1)
      if (!previous) return
      set((current) => ({
        ...previous,
        boardVersion: current.boardVersion + 1,
        history: current.history.slice(0, -1),
        activity: [event('human', 'Reversed the last board change', 'Undo created a new board version so stale agent proposals stay invalid.', current.activity.length), ...current.activity],
      }))
    },

    resetExercise: () => set((state) => ({
      ...initialData(),
      webMcpStatus: state.webMcpStatus,
      activity: [event('human', 'Exercise reset', 'The deterministic baseline was restored.', state.activity.length), ...initialActivity],
    })),

    setWebMcpStatus: (webMcpStatus) => set({ webMcpStatus }),
    readSnapshot: () => snapshot(get()),
  }))
}

export const incidentStore = createIncidentStore()
export type IncidentStore = ReturnType<typeof createIncidentStore>
