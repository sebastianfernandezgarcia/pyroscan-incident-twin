export type ZoneId = 'caldera' | 'el-paso' | 'tijarafe' | 'cumbre-vieja'

export type WindPreset = 'observed' | 'northeast-shift' | 'gusting-west'

export type HorizonMinutes = 30 | 60 | 90

export type AnnotationType = 'blocked-road' | 'priority-asset' | 'local-knowledge'

export interface Zone {
  id: ZoneId
  label: string
  sector: string
  terrain: string
  exposure: 'guarded' | 'watch' | 'elevated'
  mapPoint: readonly [number, number]
}

export interface Annotation {
  id: string
  type: AnnotationType
  zoneId: ZoneId
  note: string
  source: 'human' | 'agent'
  createdAt: string
}

export interface SpreadRing {
  minute: number
  centerX: number
  centerY: number
  radiusX: number
  radiusY: number
  rotation: number
}

export interface SpreadScenario {
  id: string
  label: string
  horizonMinutes: HorizonMinutes
  windPreset: WindPreset
  windLabel: string
  riskScore: number
  confidence: 'exercise-estimate'
  affectedZones: ZoneId[]
  watchZones: ZoneId[]
  summary: string
  rings: SpreadRing[]
  generatedAt: string
  synthetic: true
}

export type ResponseOptionId = 'ridge-hold' | 'south-anchor' | 'dual-protection'

export interface ResponseOption {
  id: ResponseOptionId
  label: string
  kicker: string
  score: number
  resourceUnits: number
  setupMinutes: number
  protects: ZoneId[]
  tradeoff: string
  recommended: boolean
}

export interface Comparison {
  scenarioId: string
  options: ResponseOption[]
  rationale: string
  generatedAt: string
}

export interface PlanAction {
  id: string
  time: string
  title: string
  detail: string
  owner: string
}

export interface ResponsePlan {
  id: string
  scenarioId: string
  optionId: ResponseOptionId
  optionLabel: string
  basedOnVersion: number
  stagedAtVersion: number
  status: 'staged' | 'needs-review' | 'approved'
  actions: PlanAction[]
  rationale: string
  stagedBy: 'agent' | 'human-demo'
}

export interface ActivityEvent {
  id: string
  at: string
  actor: 'agent' | 'human' | 'system'
  title: string
  detail: string
}

export interface IncidentSnapshot {
  boardVersion: number
  incidentId: string
  exerciseName: string
  observedAt: string
  zones: Zone[]
  annotations: Annotation[]
  scenarios: SpreadScenario[]
  activeScenario: SpreadScenario | null
  comparison: Comparison | null
  plan: ResponsePlan | null
}
