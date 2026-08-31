import { describe, expect, it } from 'vitest'
import { createIncidentStore, IncidentActionError } from './incidentStore'

describe('incident store', () => {
  it('publishes a synthetic baseline and increments the version after a simulation', () => {
    const store = createIncidentStore()
    const before = store.getState()

    before.runSimulation({ horizonMinutes: 90, windPreset: 'gusting-west' }, 'agent')
    const after = store.getState()

    expect(after.boardVersion).toBe(before.boardVersion + 1)
    expect(after.activeScenario?.id).toBe('gusting-west-90')
    expect(after.activeScenario?.synthetic).toBe(true)
    expect(after.activity[0].actor).toBe('agent')
  })

  it('rejects a plan derived from a stale board version without mutating state', () => {
    const store = createIncidentStore()
    const current = store.getState()

    expect(() => current.stagePlan({
      boardVersion: current.boardVersion - 1,
      scenarioId: current.activeScenario!.id,
      optionId: 'ridge-hold',
      rationale: 'Use the quickest exercise setup.',
    }, 'agent')).toThrowError(IncidentActionError)

    expect(store.getState().plan).toBeNull()
    expect(store.getState().boardVersion).toBe(current.boardVersion)
  })

  it('marks a staged plan for review when a human adds new local knowledge', () => {
    const store = createIncidentStore()
    const current = store.getState()
    current.stagePlan({
      boardVersion: current.boardVersion,
      scenarioId: current.activeScenario!.id,
      optionId: 'ridge-hold',
      rationale: 'Fast coverage for the active scenario.',
    }, 'agent')

    store.getState().addAnnotation({
      type: 'blocked-road',
      zoneId: 'el-paso',
      note: 'LP-3 access closed in the exercise.',
    }, 'human')

    expect(store.getState().plan?.status).toBe('needs-review')
    expect(store.getState().annotations.at(-1)?.source).toBe('human')
  })

  it('reserves final approval for the human-facing action', () => {
    const store = createIncidentStore()
    const current = store.getState()
    current.stagePlan({
      boardVersion: current.boardVersion,
      scenarioId: current.activeScenario!.id,
      optionId: 'dual-protection',
      rationale: 'Cover both exercise interfaces.',
    }, 'agent')

    expect(store.getState().plan?.status).toBe('staged')
    store.getState().approvePlan()
    expect(store.getState().plan?.status).toBe('approved')
    expect(store.getState().activity[0].actor).toBe('human')
  })
})
