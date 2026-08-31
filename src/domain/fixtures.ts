import type { ResponseOption, Zone } from './types'

export const EXERCISE_CLOCK = '2026-08-31T18:42:00.000Z'

export const ZONES: Zone[] = [
  {
    id: 'caldera',
    label: 'Caldera edge',
    sector: 'NW-01',
    terrain: 'Pine ridge / steep ravines',
    exposure: 'watch',
    mapPoint: [365, 225],
  },
  {
    id: 'tijarafe',
    label: 'Tijarafe interface',
    sector: 'W-02',
    terrain: 'Terraced interface / mixed fuel',
    exposure: 'elevated',
    mapPoint: [278, 274],
  },
  {
    id: 'el-paso',
    label: 'El Paso corridor',
    sector: 'C-03',
    terrain: 'Road corridor / urban edge',
    exposure: 'elevated',
    mapPoint: [365, 356],
  },
  {
    id: 'cumbre-vieja',
    label: 'Cumbre Vieja south',
    sector: 'S-04',
    terrain: 'Volcanic ridge / sparse access',
    exposure: 'guarded',
    mapPoint: [438, 500],
  },
]

export const RESPONSE_OPTIONS: Omit<ResponseOption, 'score' | 'recommended'>[] = [
  {
    id: 'ridge-hold',
    label: 'Hold the ridge',
    kicker: 'Fastest setup',
    resourceUnits: 4,
    setupMinutes: 18,
    protects: ['el-paso', 'caldera'],
    tradeoff: 'Leaves the western interface under observation rather than direct cover.',
  },
  {
    id: 'south-anchor',
    label: 'Anchor from the south',
    kicker: 'Safer access',
    resourceUnits: 5,
    setupMinutes: 31,
    protects: ['el-paso', 'cumbre-vieja'],
    tradeoff: 'Slower to influence the first 30-minute exercise window.',
  },
  {
    id: 'dual-protection',
    label: 'Protect both interfaces',
    kicker: 'Broadest coverage',
    resourceUnits: 7,
    setupMinutes: 26,
    protects: ['tijarafe', 'el-paso', 'caldera'],
    tradeoff: 'Consumes every reserve unit in this synthetic exercise.',
  },
]
