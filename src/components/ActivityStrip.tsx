import { Bot, ChevronRight, CircleDot, UserRound } from 'lucide-react'
import { useStore } from 'zustand'
import { incidentStore } from '../store/incidentStore'

export function ActivityStrip() {
  const activity = useStore(incidentStore, (state) => state.activity)
  return (
    <section className="activity-strip" aria-label="Shared activity timeline">
      <header>
        <div><CircleDot size={13} /><span>SHARED ACTIVITY</span></div>
        <button>Decision log <ChevronRight size={13} /></button>
      </header>
      <div className="activity-events">
        {activity.slice(0, 4).map((item, index) => (
          <article key={item.id} className={index === 0 ? 'activity-event--latest' : ''}>
            <span className={`activity-actor activity-actor--${item.actor}`}>
              {item.actor === 'agent' ? <Bot size={13} /> : item.actor === 'human' ? <UserRound size={13} /> : <CircleDot size={12} />}
            </span>
            <div><strong>{item.title}</strong><p>{item.detail}</p></div>
            <time>{item.at}</time>
          </article>
        ))}
      </div>
    </section>
  )
}
