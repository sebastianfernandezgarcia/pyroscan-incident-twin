import { AlertCircle, ArrowUpRight, Bot, Check, CheckCircle2, Clock3, RefreshCw, ShieldCheck, Sparkles, Users } from 'lucide-react'
import { useStore } from 'zustand'
import type { ResponseOptionId } from '../domain/types'
import { incidentStore } from '../store/incidentStore'

const ALL_OPTIONS: ResponseOptionId[] = ['ridge-hold', 'south-anchor', 'dual-protection']

export function DecisionPanel() {
  const activePanel = useStore(incidentStore, (state) => state.activePanel)
  const comparison = useStore(incidentStore, (state) => state.comparison)
  const scenario = useStore(incidentStore, (state) => state.activeScenario)
  const plan = useStore(incidentStore, (state) => state.plan)
  const boardVersion = useStore(incidentStore, (state) => state.boardVersion)
  const compare = useStore(incidentStore, (state) => state.compareResponseOptions)
  const stagePlan = useStore(incidentStore, (state) => state.stagePlan)
  const approvePlan = useStore(incidentStore, (state) => state.approvePlan)

  const stage = (optionId: ResponseOptionId) => {
    if (!scenario) return
    stagePlan({
      boardVersion,
      scenarioId: scenario.id,
      optionId,
      rationale: 'Balances coverage, setup time and reversible deployment in the active synthetic scenario.',
    }, 'human-demo')
  }

  const showPlan = activePanel === 'plan' && plan

  return (
    <aside className="decision-panel">
      <div className="panel-heading decision-panel__heading">
        <div>
          <p className="eyebrow">DECISION WORKBENCH</p>
          <h2>{showPlan ? 'Review the draft' : 'Compare responses'}</h2>
        </div>
        <span className="agent-chip"><Bot size={13} /> agent-ready</span>
      </div>

      {showPlan ? (
        <div className="plan-view">
          <div className={`plan-state plan-state--${plan.status}`}>
            {plan.status === 'approved' ? <CheckCircle2 size={17} /> : plan.status === 'needs-review' ? <AlertCircle size={17} /> : <Sparkles size={17} />}
            <div>
              <strong>{plan.status === 'approved' ? 'Human-approved exercise plan' : plan.status === 'needs-review' ? 'New evidence — review required' : 'Agent proposal staged'}</strong>
              <p>{plan.status === 'staged' ? 'Reversible until the exercise director approves it.' : plan.status === 'needs-review' ? 'The board changed after this plan was staged.' : 'Approval was completed in the human interface.'}</p>
            </div>
          </div>

          <div className="plan-summary">
            <p className="eyebrow">SELECTED APPROACH</p>
            <h3>{plan.optionLabel}</h3>
            <p>{plan.rationale}</p>
            <span>Based on board v{plan.basedOnVersion} · scenario {plan.scenarioId}</span>
          </div>

          <ol className="plan-actions">
            {plan.actions.map((action, index) => (
              <li key={action.id}>
                <span className="plan-actions__index">{String(index + 1).padStart(2, '0')}</span>
                <div><strong>{action.title}</strong><p>{action.detail}</p><small>{action.owner}</small></div>
                <time>{action.time}</time>
              </li>
            ))}
          </ol>

          {plan.status === 'staged' ? (
            <button className="approve-button" onClick={approvePlan}><ShieldCheck size={16} /> Approve exercise plan</button>
          ) : plan.status === 'needs-review' ? (
            <button className="primary-button decision-full" onClick={() => stage(plan.optionId)}><RefreshCw size={15} /> Restage against v{boardVersion}</button>
          ) : (
            <div className="approved-receipt"><Check size={14} /> Human decision gate complete</div>
          )}
          <p className="human-only"><Users size={13} /> Final approval is deliberately not exposed as a WebMCP tool.</p>
        </div>
      ) : (
        <div className="comparison-view">
          <div className="scenario-summary">
            <div><span>ACTIVE SCENARIO</span><strong>{scenario?.label}</strong></div>
            <span className="scenario-summary__score">{scenario?.riskScore}<small>/100</small></span>
          </div>

          {!comparison ? (
            <button className="generate-comparison" onClick={() => compare(ALL_OPTIONS, 'human')}>
              <Sparkles size={16} /> Compare all response options
            </button>
          ) : (
            <>
              <div className="option-stack">
                {comparison.options.map((option) => (
                  <article className={`option-card ${option.recommended ? 'option-card--recommended' : ''}`} key={option.id}>
                    <div className="option-card__top">
                      <div>
                        <span>{option.kicker}</span>
                        <h3>{option.label}</h3>
                      </div>
                      <div className="option-score"><strong>{option.score}</strong><small>fit</small></div>
                    </div>
                    <div className="option-metrics">
                      <span><Clock3 size={13} /> {option.setupMinutes} min</span>
                      <span><Users size={13} /> {option.resourceUnits} units</span>
                      <span><CheckCircle2 size={13} /> {option.protects.length} sectors</span>
                    </div>
                    <p>{option.tradeoff}</p>
                    <button onClick={() => stage(option.id)}>
                      Stage for review <ArrowUpRight size={14} />
                    </button>
                    {option.recommended ? <span className="recommended-tag"><Sparkles size={11} /> MODEL FIT</span> : null}
                  </article>
                ))}
              </div>
              <div className="comparison-rationale">
                <Bot size={15} />
                <p><strong>Why this ranking</strong>{comparison.rationale}</p>
              </div>
              <button className="text-button" onClick={() => compare(ALL_OPTIONS, 'human')}><RefreshCw size={13} /> Recalculate with current board</button>
            </>
          )}
        </div>
      )}
    </aside>
  )
}
