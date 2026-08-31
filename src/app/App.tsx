import { useState } from 'react'
import { AlertTriangle, ArrowLeft, Check, Clipboard, RotateCcw, Sparkles, Undo2, X } from 'lucide-react'
import { useStore } from 'zustand'
import { ActivityStrip } from '../components/ActivityStrip'
import { DecisionPanel } from '../components/DecisionPanel'
import { EvidenceRail } from '../components/EvidenceRail'
import { IncidentMap } from '../components/IncidentMap'
import { incidentStore } from '../store/incidentStore'

export function App() {
  const boardVersion = useStore(incidentStore, (state) => state.boardVersion)
  const exerciseName = useStore(incidentStore, (state) => state.exerciseName)
  const webMcpStatus = useStore(incidentStore, (state) => state.webMcpStatus)
  const canUndo = useStore(incidentStore, (state) => state.history.length > 0)
  const undoLastChange = useStore(incidentStore, (state) => state.undoLastChange)
  const resetExercise = useStore(incidentStore, (state) => state.resetExercise)
  const [showBrief, setShowBrief] = useState(false)
  const [promptCopied, setPromptCopied] = useState(false)

  const judgePrompt = 'Inspect El Paso. Add a blocked-road exercise note for the LP-3 checkpoint. Simulate a 60-minute northeast wind shift, compare the ridge and dual-interface options, then stage the safest reversible plan.'

  const copyJudgePrompt = async () => {
    await navigator.clipboard?.writeText(judgePrompt)
    setPromptCopied(true)
    window.setTimeout(() => setPromptCopied(false), 1800)
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand-lockup">
          <div className="brand-mark" aria-hidden="true">
            <span />
            <span />
            <span />
          </div>
          <div>
            <p className="eyebrow">PYROSCAN</p>
            <h1>Incident Twin</h1>
          </div>
        </div>

        <div className="incident-identity">
          <span className="incident-identity__back" aria-hidden="true"><ArrowLeft size={14} /></span>
          <div>
            <p className="eyebrow">EXERCISE LP-EX-042</p>
            <strong>{exerciseName}</strong>
          </div>
          <span className="version-pill">v{boardVersion}</span>
        </div>

        <div className="topbar-actions">
          <button
            className="quiet-button"
            onClick={() => setShowBrief((value) => !value)}
            aria-expanded={showBrief}
            aria-controls="collaboration-guide"
          >
            <Sparkles size={15} /> How it works
          </button>
          <button className="icon-button" onClick={undoLastChange} disabled={!canUndo} aria-label="Undo last board change">
            <Undo2 size={16} />
          </button>
          <button className="icon-button" onClick={resetExercise} aria-label="Reset exercise">
            <RotateCcw size={16} />
          </button>
          <div className={`webmcp-status webmcp-status--${webMcpStatus}`}>
            <span className="status-orbit" aria-hidden="true" />
            <div>
              <small>WEBMCP</small>
              <strong>{webMcpStatus === 'available' ? '6 tools live' : webMcpStatus === 'checking' ? 'checking' : 'browser preview'}</strong>
            </div>
          </div>
        </div>
      </header>

      <div className="safety-ribbon" role="note">
        <span><AlertTriangle size={14} /> SYNTHETIC EXERCISE</span>
        <p>No live incident data. No dispatch or emergency decisions. Every proposal requires human review.</p>
        <span className="safety-ribbon__right">LOCAL-FIRST · DETERMINISTIC</span>
      </div>

      {showBrief ? (
        <aside className="collaboration-guide" id="collaboration-guide" aria-label="Human and agent collaboration guide">
          <div className="collaboration-guide__intro">
            <p className="eyebrow">BEFORE A LIVE INCIDENT</p>
            <strong>Rehearse decisions on one shared map.</strong>
            <span>People contribute context. The agent explores bounded alternatives. The human stays in command.</span>
          </div>

          <ol className="collaboration-guide__steps">
            <li><span>01</span><div><strong>Human grounds</strong><small>Add routes, assets and local knowledge.</small></div></li>
            <li><span>02</span><div><strong>Agent rehearses</strong><small>Inspect, simulate and compare through WebMCP.</small></div></li>
            <li><span>03</span><div><strong>Human decides</strong><small>Review the reversible draft and approve.</small></div></li>
          </ol>

          <div className="collaboration-guide__prompt">
            <p className="eyebrow">JUDGE PROMPT</p>
            <span>“{judgePrompt}”</span>
            <button onClick={copyJudgePrompt} aria-live="polite">
              {promptCopied ? <Check size={14} /> : <Clipboard size={14} />}
              {promptCopied ? 'Copied' : 'Copy prompt'}
            </button>
          </div>

          <button className="collaboration-guide__close" onClick={() => setShowBrief(false)} aria-label="Close how it works">
            <X size={15} />
          </button>
        </aside>
      ) : null}

      <main className="workspace">
        <EvidenceRail />
        <section className="map-column" aria-label="Shared incident map">
          <IncidentMap />
          <ActivityStrip />
        </section>
        <DecisionPanel />
      </main>
    </div>
  )
}
