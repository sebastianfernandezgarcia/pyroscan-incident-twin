import { describe, expect, it } from 'vitest'
import { compareOptions, simulateSpread } from './simulator'

describe('simulateSpread', () => {
  it('is deterministic for the same exercise inputs', () => {
    const first = simulateSpread({ horizonMinutes: 60, windPreset: 'observed', annotations: [] })
    const second = simulateSpread({ horizonMinutes: 60, windPreset: 'observed', annotations: [] })

    expect(first).toEqual(second)
    expect(first.synthetic).toBe(true)
    expect(first.confidence).toBe('exercise-estimate')
    expect(first.rings).toHaveLength(3)
  })

  it('makes a priority asset visible in the affected-zone assessment', () => {
    const scenario = simulateSpread({
      horizonMinutes: 30,
      windPreset: 'northeast-shift',
      annotations: [{
        id: 'a-1',
        type: 'priority-asset',
        zoneId: 'caldera',
        note: 'Exercise water relay',
        source: 'human',
        createdAt: '2026-08-31T18:42:00.000Z',
      }],
    })

    expect(scenario.affectedZones).toContain('caldera')
    expect(scenario.riskScore).toBeGreaterThanOrEqual(68)
  })
})

describe('compareOptions', () => {
  it('scores only requested options and returns a single recommendation', () => {
    const scenario = simulateSpread({ horizonMinutes: 60, windPreset: 'gusting-west', annotations: [] })
    const comparison = compareOptions(scenario, ['ridge-hold', 'dual-protection'], [])

    expect(comparison.options.map((option) => option.id)).toEqual(['ridge-hold', 'dual-protection'])
    expect(comparison.options.filter((option) => option.recommended)).toHaveLength(1)
    expect(comparison.rationale).toContain('synthetic')
  })
})
