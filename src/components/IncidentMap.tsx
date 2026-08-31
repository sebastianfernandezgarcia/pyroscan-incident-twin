import { useState } from 'react'
import { Box, Check, ChevronDown, Compass, Layers3, Play, Wind } from 'lucide-react'
import { useStore } from 'zustand'
import type { HorizonMinutes, WindPreset, ZoneId } from '../domain/types'
import { incidentStore } from '../store/incidentStore'

const WIND_LABELS: Record<WindPreset, string> = {
  observed: 'Observed ENE',
  'northeast-shift': 'NE shift',
  'gusting-west': 'West gusts',
}

const ZONE_SHORT: Record<ZoneId, string> = {
  caldera: 'CALDERA',
  tijarafe: 'TIJARAFE',
  'el-paso': 'EL PASO',
  'cumbre-vieja': 'CUMBRE VIEJA',
}

export function IncidentMap() {
  const scenario = useStore(incidentStore, (state) => state.activeScenario)
  const zones = useStore(incidentStore, (state) => state.zones)
  const annotations = useStore(incidentStore, (state) => state.annotations)
  const focusedZoneId = useStore(incidentStore, (state) => state.focusedZoneId)
  const inspectZone = useStore(incidentStore, (state) => state.inspectZone)
  const runSimulation = useStore(incidentStore, (state) => state.runSimulation)
  const [wind, setWind] = useState<WindPreset>(scenario?.windPreset ?? 'observed')
  const [horizon, setHorizon] = useState<HorizonMinutes>(scenario?.horizonMinutes ?? 60)

  return (
    <section className="map-card">
      <header className="map-toolbar">
        <div className="map-toolbar__title">
          <span><Layers3 size={15} /></span>
          <div><p className="eyebrow">SHARED INCIDENT SURFACE</p><strong>Live exercise map</strong></div>
        </div>
        <div className="map-controls">
          <label className="select-control">
            <Wind size={14} />
            <select value={wind} onChange={(event) => setWind(event.target.value as WindPreset)} aria-label="Wind scenario">
              {Object.entries(WIND_LABELS).map(([value, label]) => <option value={value} key={value}>{label}</option>)}
            </select>
            <ChevronDown size={13} />
          </label>
          <div className="segmented-control" aria-label="Simulation horizon">
            {([30, 60, 90] as HorizonMinutes[]).map((minutes) => (
              <button key={minutes} className={horizon === minutes ? 'active' : ''} onClick={() => setHorizon(minutes)}>{minutes}m</button>
            ))}
          </div>
          <button className="simulate-button" onClick={() => runSimulation({ horizonMinutes: horizon, windPreset: wind }, 'human')}>
            <Play size={13} fill="currentColor" /> Simulate
          </button>
        </div>
      </header>

      <div className="map-stage">
        <div className="scenario-float">
          <p><Box size={13} /> ACTIVE SYNTHETIC MODEL</p>
          <strong>{scenario?.label ?? 'No scenario'}</strong>
          <span>{scenario?.windLabel}</span>
        </div>
        <div className="risk-float">
          <span className="risk-float__number">{scenario?.riskScore ?? '—'}</span>
          <span><small>ATTENTION</small><strong>exercise index</strong></span>
        </div>

        <svg className="incident-map" viewBox="0 0 800 700" role="img" aria-label="Synthetic exercise map of La Palma with spread contours and response sectors">
          <defs>
            <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#131816" />
              <stop offset="100%" stopColor="#090b0a" />
            </linearGradient>
            <linearGradient id="island" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#29312d" />
              <stop offset="45%" stopColor="#222824" />
              <stop offset="100%" stopColor="#161b18" />
            </linearGradient>
            <radialGradient id="fireCore">
              <stop offset="0%" stopColor="#fff4bf" />
              <stop offset="35%" stopColor="#ff9d54" />
              <stop offset="100%" stopColor="#ff4f26" />
            </radialGradient>
            <pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse">
              <path d="M 38 0 L 0 0 0 38" fill="none" stroke="#a5b4a9" strokeOpacity="0.055" strokeWidth="1" />
            </pattern>
            <filter id="glow"><feGaussianBlur stdDeviation="9" /></filter>
          </defs>
          <rect width="800" height="700" fill="url(#sea)" />
          <rect width="800" height="700" fill="url(#grid)" />

          <g className="map-coordinates" aria-hidden="true">
            <text x="24" y="35">28°48'N</text><text x="24" y="675">28°26'N</text>
            <text x="684" y="35">17°43'W</text><text x="684" y="675">17°56'W</text>
          </g>

          <path
            className="island-shape"
            d="M398 40 C338 51 302 92 286 137 C267 190 230 220 219 275 C209 325 224 365 248 400 C273 437 298 461 314 504 C331 549 340 627 393 657 C445 686 490 633 509 585 C528 536 557 502 567 449 C576 398 554 359 548 314 C542 269 568 220 539 178 C513 140 478 125 463 81 C453 52 427 35 398 40 Z"
            fill="url(#island)"
            stroke="#78877c"
            strokeOpacity="0.42"
            strokeWidth="2"
          />

          <g className="contour-lines" aria-hidden="true">
            <path d="M301 155 C347 115 446 106 509 168 C557 216 540 277 494 301 C447 327 365 313 316 273 C274 240 267 193 301 155 Z" />
            <path d="M280 224 C318 185 377 170 432 184 C489 199 522 239 513 280 C504 320 455 351 396 347 C334 343 281 314 268 275" />
            <path d="M280 405 C328 370 411 357 478 389 C532 416 546 469 521 507 C493 548 430 564 371 544 C316 526 276 481 280 405 Z" />
            <path d="M334 505 C370 478 441 479 480 520 C513 555 503 606 463 627 C421 650 369 629 348 589 C334 563 326 530 334 505 Z" />
          </g>

          <g className="road-network" aria-label="Synthetic access routes">
            <path d="M303 180 C340 224 366 283 403 347 C436 404 457 470 468 577" />
            <path d="M242 337 C306 349 355 363 414 403 C462 436 505 451 552 438" />
            <path d="M277 430 C337 423 384 410 428 377 C463 350 501 307 535 255" />
            <path d="M343 116 C380 144 421 148 468 131" />
          </g>

          {scenario?.rings.slice().reverse().map((ring, index) => (
            <ellipse
              key={ring.minute}
              className={`spread-ring spread-ring--${index}`}
              cx={ring.centerX}
              cy={ring.centerY}
              rx={ring.radiusX}
              ry={ring.radiusY}
              transform={`rotate(${ring.rotation} ${ring.centerX} ${ring.centerY})`}
            />
          ))}

          <g className="ignition-marker" transform="translate(420 402)" aria-label="Synthetic exercise ignition">
            <circle r="28" className="ignition-marker__glow" filter="url(#glow)" />
            <circle r="8" fill="url(#fireCore)" />
            <circle r="15" fill="none" stroke="#ff7a3d" strokeOpacity="0.45" />
          </g>

          <g className="wind-arrow" transform="translate(625 122)">
            <circle r="41" />
            <path d="M-21 6 L21 -8 M13 -15 L21 -8 L14 0" />
            <text x="0" y="56">ENE 18</text>
          </g>

          {annotations.map((annotation, index) => {
            const zone = zones.find((candidate) => candidate.id === annotation.zoneId)
            if (!zone) return null
            return (
              <g key={annotation.id} className="annotation-marker" transform={`translate(${zone.mapPoint[0] + 24 + index * 3} ${zone.mapPoint[1] - 17})`}>
                <path d="M0 -10 L9 7 L-9 7 Z" />
                <text y="4">!</text>
              </g>
            )
          })}

          {zones.map((zone) => {
            const affected = scenario?.affectedZones.includes(zone.id)
            const watch = scenario?.watchZones.includes(zone.id)
            const focused = focusedZoneId === zone.id
            return (
              <g
                key={zone.id}
                className={`zone-marker ${affected ? 'zone-marker--affected' : watch ? 'zone-marker--watch' : ''} ${focused ? 'zone-marker--focused' : ''}`}
                transform={`translate(${zone.mapPoint[0]} ${zone.mapPoint[1]})`}
                role="button"
                tabIndex={0}
                onClick={() => inspectZone(zone.id, 'human')}
                onKeyDown={(event) => event.key === 'Enter' && inspectZone(zone.id, 'human')}
                aria-label={`Inspect ${zone.label}`}
              >
                <circle r="11" className="zone-marker__outer" />
                <circle r="4" className="zone-marker__inner" />
                <text x="17" y="-5">{ZONE_SHORT[zone.id]}</text>
                <text x="17" y="10" className="zone-marker__sector">{zone.sector}</text>
              </g>
            )
          })}

          <g className="north-arrow" transform="translate(70 585)">
            <path d="M0 -25 L9 7 L0 2 L-9 7 Z" />
            <text y="25">N</text>
          </g>
        </svg>

        <div className="map-legend">
          <span><i className="legend-fire" /> exercise origin</span>
          <span><i className="legend-contour" /> modeled attention area</span>
          <span><i className="legend-zone" /> sector</span>
          <span className="map-legend__truth"><Check size={12} /> all data is synthetic</span>
        </div>
        <div className="map-tools" aria-hidden="true"><button><Compass size={16} /></button><button><Layers3 size={16} /></button></div>
      </div>
    </section>
  )
}
