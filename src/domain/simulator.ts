import { EXERCISE_CLOCK, RESPONSE_OPTIONS } from './fixtures'
import type {
  Annotation,
  Comparison,
  HorizonMinutes,
  ResponseOptionId,
  SpreadRing,
  SpreadScenario,
  WindPreset,
  ZoneId,
} from './types'

interface SimulationInput {
  horizonMinutes: HorizonMinutes
  windPreset: WindPreset
  annotations: Annotation[]
}

const WIND: Record<WindPreset, {
  label: string
  dx: number
  dy: number
  rotation: number
  risk: number
}> = {
  observed: { label: 'ENE 18 km/h · observed fixture', dx: 1, dy: 0.26, rotation: 14, risk: 61 },
  'northeast-shift': { label: 'NE shift 26 km/h · what-if', dx: 0.48, dy: -0.88, rotation: -28, risk: 69 },
  'gusting-west': { label: 'W gusts 34 km/h · what-if', dx: -1, dy: 0.16, rotation: -8, risk: 74 },
}

const UNIQUE = <T,>(items: T[]) => [...new Set(items)]

function affectedFor(windPreset: WindPreset, horizonMinutes: HorizonMinutes): {
  affected: ZoneId[]
  watch: ZoneId[]
} {
  if (windPreset === 'northeast-shift') {
    return horizonMinutes === 30
      ? { affected: ['caldera'], watch: ['el-paso'] }
      : { affected: ['caldera', 'el-paso'], watch: ['tijarafe'] }
  }
  if (windPreset === 'gusting-west') {
    return horizonMinutes === 30
      ? { affected: ['tijarafe'], watch: ['el-paso'] }
      : { affected: ['tijarafe', 'el-paso'], watch: ['caldera'] }
  }
  if (horizonMinutes === 30) return { affected: ['el-paso'], watch: ['tijarafe'] }
  if (horizonMinutes === 60) return { affected: ['el-paso', 'tijarafe'], watch: ['caldera'] }
  return { affected: ['el-paso', 'tijarafe', 'caldera'], watch: ['cumbre-vieja'] }
}

function ringsFor(horizonMinutes: HorizonMinutes, windPreset: WindPreset): SpreadRing[] {
  const wind = WIND[windPreset]
  const steps = horizonMinutes === 30 ? [10, 20, 30] : horizonMinutes === 60 ? [20, 40, 60] : [30, 60, 90]
  return steps.map((minute) => {
    const scale = minute / 30
    return {
      minute,
      centerX: Math.round(394 + wind.dx * 19 * scale),
      centerY: Math.round(390 + wind.dy * 19 * scale),
      radiusX: Math.round(42 + scale * (48 + Math.abs(wind.dx) * 12)),
      radiusY: Math.round(30 + scale * (34 + Math.abs(wind.dy) * 10)),
      rotation: wind.rotation,
    }
  })
}

export function simulateSpread({ horizonMinutes, windPreset, annotations }: SimulationInput): SpreadScenario {
  const wind = WIND[windPreset]
  const zones = affectedFor(windPreset, horizonMinutes)
  const priorityZones = annotations
    .filter((annotation) => annotation.type === 'priority-asset')
    .map((annotation) => annotation.zoneId)
  const blockedRoads = annotations.filter((annotation) => annotation.type === 'blocked-road').length
  const horizonRisk = horizonMinutes === 30 ? 0 : horizonMinutes === 60 ? 5 : 9
  const riskScore = Math.min(94, wind.risk + horizonRisk + priorityZones.length * 3 + blockedRoads * 2)

  const affectedZones = UNIQUE([...zones.affected, ...priorityZones])
  const watchZones = zones.watch.filter((zone) => !affectedZones.includes(zone))

  return {
    id: `${windPreset}-${horizonMinutes}`,
    label: `${horizonMinutes} min · ${windPreset === 'observed' ? 'Observed wind' : 'What-if wind'}`,
    horizonMinutes,
    windPreset,
    windLabel: wind.label,
    riskScore,
    confidence: 'exercise-estimate',
    affectedZones,
    watchZones,
    summary: `${affectedZones.length} exercise sector${affectedZones.length === 1 ? '' : 's'} in the attention area; ${watchZones.length} on watch.`,
    rings: ringsFor(horizonMinutes, windPreset),
    generatedAt: EXERCISE_CLOCK,
    synthetic: true,
  }
}

export function compareOptions(
  scenario: SpreadScenario,
  optionIds: ResponseOptionId[],
  annotations: Annotation[],
): Comparison {
  const blockedZones = new Set(
    annotations.filter((annotation) => annotation.type === 'blocked-road').map((annotation) => annotation.zoneId),
  )
  const options = RESPONSE_OPTIONS
    .filter((option) => optionIds.includes(option.id))
    .map((option) => {
      const directCoverage = option.protects.filter((zone) => scenario.affectedZones.includes(zone)).length
      const watchCoverage = option.protects.filter((zone) => scenario.watchZones.includes(zone)).length
      const blockedPenalty = option.protects.some((zone) => blockedZones.has(zone)) ? 9 : 0
      const reservePenalty = option.resourceUnits > 6 ? 4 : 0
      const score = Math.max(1, Math.min(99,
        48 + directCoverage * 17 + watchCoverage * 6 - Math.round(option.setupMinutes / 7) - blockedPenalty - reservePenalty,
      ))
      return { ...option, score, recommended: false }
    })
    .sort((a, b) => optionIds.indexOf(a.id) - optionIds.indexOf(b.id))

  const best = options.reduce((winner, option) => option.score > winner.score ? option : winner, options[0])
  const scored = options.map((option) => ({ ...option, recommended: option.id === best.id }))

  return {
    scenarioId: scenario.id,
    options: scored,
    rationale: `${best.label} has the strongest coverage-to-readiness score in this synthetic exercise. Human review is still required.`,
    generatedAt: EXERCISE_CLOCK,
  }
}
