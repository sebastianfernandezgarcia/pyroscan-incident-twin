import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createIncidentStore } from '../store/incidentStore'
import { startIncidentTools } from './registerIncidentTools'

describe('PyroScan WebMCP registration', () => {
  const registered: WebMCP.ModelContextTool[] = []

  beforeEach(() => {
    registered.length = 0
    Object.defineProperty(document, 'modelContext', {
      configurable: true,
      value: {
        registerTool: vi.fn(async (tool: WebMCP.ModelContextTool) => { registered.push(tool) }),
      },
    })
  })

  it('registers six intent-level tools and deliberately omits human approval', async () => {
    const store = createIncidentStore()
    const registration = startIncidentTools(store)
    await registration.ready

    expect(registered.map((tool) => tool.name)).toEqual([
      'read_incident_board',
      'inspect_zone',
      'simulate_spread',
      'compare_response_options',
      'stage_response_plan',
      'add_board_annotation',
    ])
    expect(registered.some((tool) => tool.name.includes('approve'))).toBe(false)
    expect(registered.find((tool) => tool.name === 'read_incident_board')?.annotations?.readOnlyHint).toBe(true)
    expect(store.getState().webMcpStatus).toBe('available')
  })

  it('uses the same state as the visual board and rejects stale staging', async () => {
    const store = createIncidentStore()
    const registration = startIncidentTools(store)
    await registration.ready
    const options = { signal: new AbortController().signal }
    const simulate = registered.find((tool) => tool.name === 'simulate_spread')!
    const stage = registered.find((tool) => tool.name === 'stage_response_plan')!

    const beforeVersion = store.getState().boardVersion
    await simulate.execute({ horizonMinutes: 90, windPreset: 'northeast-shift' }, options)

    expect(store.getState().activeScenario?.id).toBe('northeast-shift-90')
    expect(store.getState().boardVersion).toBe(beforeVersion + 1)
    await expect(stage.execute({
      boardVersion: beforeVersion,
      scenarioId: 'northeast-shift-90',
      optionId: 'ridge-hold',
      rationale: 'Use the fastest reversible exercise setup.',
    }, options)).rejects.toThrow(/STALE_BOARD/)
  })

  it('unregisters all tools by aborting one lifecycle signal', async () => {
    const store = createIncidentStore()
    const registration = startIncidentTools(store)
    await registration.ready
    const calls = vi.mocked(document.modelContext!.registerTool).mock.calls

    expect(calls.every((call) => call[1]?.signal === registration.controller.signal)).toBe(true)
    registration.controller.abort()
    expect(registration.controller.signal.aborted).toBe(true)
  })

  it('accepts hosts that provide callback options without an execution signal', async () => {
    const store = createIncidentStore()
    const registration = startIncidentTools(store)
    await registration.ready
    const read = registered.find((tool) => tool.name === 'read_incident_board')!

    await expect(read.execute({}, {} as WebMCP.ToolExecuteCallbackOptions)).resolves.toMatchObject({ ok: true })
  })
})
