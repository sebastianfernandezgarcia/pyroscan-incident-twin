import { useState, type FormEvent } from 'react'
import { AlertOctagon, ChevronRight, CloudSun, History, MapPin, Mountain, Plus, Radio, X } from 'lucide-react'
import { useStore } from 'zustand'
import type { AnnotationType, ZoneId } from '../domain/types'
import { incidentStore } from '../store/incidentStore'

const SOURCE_ROWS = [
  {
    icon: History,
    label: 'Copernicus EMSR671',
    value: '2,117 ha',
    provenance: 'observed burn scar · 2023',
    tone: 'blue',
    href: 'https://mapping.emergency.copernicus.eu/activations/EMSR671/',
  },
  {
    icon: Mountain,
    label: 'SITCAN terrain',
    value: '25 m',
    provenance: 'public MDT · updated 2021',
    tone: 'mint',
    href: 'https://opendata.sitcan.es/dataset/modelo-digital-de-terreno-mdt-de-25x25-metros/resource/90d97840-9bc9-4e31-a470-3cb631806fd5',
  },
  {
    icon: CloudSun,
    label: 'Exercise inputs',
    value: 'ENE 18',
    provenance: 'synthetic fixture',
    tone: 'amber',
    href: null,
  },
] as const

const TYPE_LABELS: Record<AnnotationType, string> = {
  'blocked-road': 'Blocked road',
  'priority-asset': 'Priority asset',
  'local-knowledge': 'Local knowledge',
}

export function EvidenceRail() {
  const zones = useStore(incidentStore, (state) => state.zones)
  const annotations = useStore(incidentStore, (state) => state.annotations)
  const focusedZoneId = useStore(incidentStore, (state) => state.focusedZoneId)
  const inspectZone = useStore(incidentStore, (state) => state.inspectZone)
  const addAnnotation = useStore(incidentStore, (state) => state.addAnnotation)
  const [showForm, setShowForm] = useState(false)
  const [zoneId, setZoneId] = useState<ZoneId>('el-paso')
  const [type, setType] = useState<AnnotationType>('blocked-road')
  const [note, setNote] = useState('LP-3 closed at the exercise checkpoint')

  const submit = (event: FormEvent) => {
    event.preventDefault()
    addAnnotation({ type, zoneId, note }, 'human')
    setShowForm(false)
  }

  return (
    <aside className="evidence-rail">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">EVIDENCE DESK</p>
          <h2>What we know</h2>
        </div>
        <span className="live-dot"><Radio size={12} /> 18:42Z</span>
      </div>

      <section className="source-stack" aria-label="Public context and synthetic exercise sources">
        {SOURCE_ROWS.map(({ icon: Icon, label, value, provenance, tone, href }) => (
          <article className="source-row" key={label}>
            <span className={`source-icon source-icon--${tone}`}><Icon size={15} /></span>
            <div>
              {href ? <a href={href} target="_blank" rel="noreferrer"><strong>{label}</strong></a> : <strong>{label}</strong>}
              <small>{provenance}</small>
            </div>
            <span>{value}</span>
          </article>
        ))}
      </section>
      <p className="public-data-note">
        Public layers provide historical and terrain context only. They do not drive the active what-if.{' '}
        <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">Coastline © OpenStreetMap contributors.</a>
      </p>

      <section className="rail-section">
        <div className="rail-section__title">
          <p className="eyebrow">SECTOR WATCH</p>
          <span>{zones.length}</span>
        </div>
        <div className="zone-list">
          {zones.map((zone) => (
            <button
              key={zone.id}
              className={`zone-row ${focusedZoneId === zone.id ? 'zone-row--active' : ''}`}
              onClick={() => inspectZone(zone.id, 'human')}
            >
              <span className={`exposure-dot exposure-dot--${zone.exposure}`} />
              <span><strong>{zone.label}</strong><small>{zone.sector} · {zone.terrain}</small></span>
              <ChevronRight size={15} />
            </button>
          ))}
        </div>
      </section>

      <section className="rail-section local-knowledge">
        <div className="rail-section__title">
          <div>
            <p className="eyebrow">LOCAL KNOWLEDGE</p>
            <small>Visible to the agent</small>
          </div>
          <span>{annotations.length}</span>
        </div>

        {annotations.length ? (
          <div className="annotation-list">
            {annotations.slice(-3).reverse().map((annotation) => (
              <article key={annotation.id} className="annotation-card">
                <AlertOctagon size={14} />
                <div>
                  <strong>{TYPE_LABELS[annotation.type]}</strong>
                  <p>{annotation.note}</p>
                  <small>{zones.find((zone) => zone.id === annotation.zoneId)?.label} · {annotation.source}</small>
                </div>
              </article>
            ))}
          </div>
        ) : (
          <p className="empty-copy">Add context that sensors cannot know: closures, vulnerable assets or local priorities.</p>
        )}

        {!showForm ? (
          <button className="add-knowledge" onClick={() => setShowForm(true)}><Plus size={15} /> Add local knowledge</button>
        ) : (
          <form className="knowledge-form" onSubmit={submit}>
            <button type="button" className="knowledge-form__close" onClick={() => setShowForm(false)} aria-label="Close annotation form"><X size={14} /></button>
            <label>Type
              <select value={type} onChange={(event) => setType(event.target.value as AnnotationType)}>
                {Object.entries(TYPE_LABELS).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
              </select>
            </label>
            <label>Sector
              <select value={zoneId} onChange={(event) => setZoneId(event.target.value as ZoneId)}>
                {zones.map((zone) => <option value={zone.id} key={zone.id}>{zone.label}</option>)}
              </select>
            </label>
            <label>Observation
              <textarea value={note} maxLength={280} onChange={(event) => setNote(event.target.value)} />
            </label>
            <button className="primary-button" type="submit"><MapPin size={14} /> Pin to board</button>
          </form>
        )}
      </section>
    </aside>
  )
}
