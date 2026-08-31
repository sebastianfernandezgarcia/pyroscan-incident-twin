import { useEffect, useState } from 'react'
import { Box, Check, ChevronDown, Compass, Layers3, Play, Wind } from 'lucide-react'
import { useStore } from 'zustand'
import { LA_PALMA_PATH } from '../domain/laPalmaGeometry'
import type { HorizonMinutes, WindPreset, ZoneId } from '../domain/types'
import { incidentStore } from '../store/incidentStore'

const FIRE_ORIGIN = { x: 394, y: 390 } as const

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

const WIND_MAP: Record<WindPreset, { label: string; rotation: number }> = {
  observed: { label: 'ENE 18', rotation: 0 },
  'northeast-shift': { label: 'NE 26', rotation: -36 },
  'gusting-west': { label: 'W 34', rotation: 154 },
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

  useEffect(() => {
    if (!scenario) return
    setWind(scenario.windPreset)
    setHorizon(scenario.horizonMinutes)
  }, [scenario])

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

        <svg className="incident-map" viewBox="0 0 800 700" role="img" aria-label="Geographically accurate synthetic exercise map of La Palma with animated fire spread and response sectors">
          <defs>
            <linearGradient id="sea" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#121a17" />
              <stop offset="55%" stopColor="#0a0e0c" />
              <stop offset="100%" stopColor="#070908" />
            </linearGradient>
            <linearGradient id="island" x1="0" y1="0" x2="1" y2="1">
              <stop offset="0%" stopColor="#39423b" />
              <stop offset="38%" stopColor="#2a312c" />
              <stop offset="72%" stopColor="#202720" />
              <stop offset="100%" stopColor="#151a16" />
            </linearGradient>
            <radialGradient id="caldera" cx="48%" cy="40%" r="58%">
              <stop offset="0%" stopColor="#111713" />
              <stop offset="64%" stopColor="#2d3830" />
              <stop offset="100%" stopColor="#171c18" />
            </radialGradient>
            <radialGradient id="fireCore">
              <stop offset="0%" stopColor="#fff4bf" />
              <stop offset="35%" stopColor="#ff9d54" />
              <stop offset="100%" stopColor="#ff4f26" />
            </radialGradient>
            <pattern id="grid" width="38" height="38" patternUnits="userSpaceOnUse">
              <path d="M 38 0 L 0 0 0 38" fill="none" stroke="#a5b4a9" strokeOpacity="0.055" strokeWidth="1" />
            </pattern>
            <filter id="glow"><feGaussianBlur stdDeviation="9" /></filter>
            <filter id="islandShadow" x="-40%" y="-30%" width="180%" height="180%">
              <feGaussianBlur stdDeviation="13" />
            </filter>
            <clipPath id="islandClip"><path d={LA_PALMA_PATH} /></clipPath>
          </defs>
          <rect width="800" height="700" fill="url(#sea)" />
          <rect width="800" height="700" fill="url(#grid)" />

          <g className="ocean-depth" aria-hidden="true">
            <path d="M125 91 C268 11 557 4 692 103" />
            <path d="M98 603 C252 690 568 693 711 582" />
          </g>

          <g className="map-coordinates" aria-hidden="true">
            <text x="24" y="35">28°52'N</text><text x="24" y="675">28°27'N</text>
            <text x="684" y="35">17°43'W</text><text x="684" y="675">18°00'W</text>
          </g>

          <path className="island-shadow" d={LA_PALMA_PATH} />
          <path className="island-shape" d={LA_PALMA_PATH} fill="url(#island)" />

          <g clipPath="url(#islandClip)" className="island-terrain" aria-hidden="true">
            <ellipse cx="398" cy="210" rx="127" ry="109" fill="url(#caldera)" opacity=".72" />
            <path className="ridge-spine" d="M416 288 C403 331 414 372 411 417 C408 471 427 518 431 610" />
            <path className="ridge-shadow" d="M448 276 C435 326 448 367 447 418 C446 477 465 520 466 585" />
            <g className="terrain-ridges">
              <path d="M279 122 C326 86 419 75 492 104 C547 126 565 176 536 215 C506 257 434 279 360 262 C296 247 260 198 279 122 Z" />
              <path d="M302 144 C343 113 414 107 474 130 C519 147 531 184 508 213 C480 247 423 257 368 245 C321 234 288 194 302 144 Z" />
              <path d="M330 163 C365 140 416 139 455 154 C488 167 493 190 475 211 C452 236 409 239 371 226 C341 215 319 189 330 163 Z" />
              <path d="M302 286 C350 268 432 272 486 304 C527 329 535 362 512 385 C484 413 423 416 365 392 C319 373 287 330 302 286 Z" />
              <path d="M319 362 C359 340 425 345 473 377 C513 404 519 444 494 468 C465 496 409 493 365 466 C326 442 301 397 319 362 Z" />
              <path d="M345 442 C377 423 429 429 468 457 C501 480 505 516 483 537 C458 561 416 556 382 535 C350 516 329 473 345 442 Z" />
              <path d="M371 522 C396 507 437 513 465 536 C489 555 487 584 470 602 C449 623 416 617 394 598 C374 581 358 543 371 522 Z" />
            </g>
            <g className="forest-texture">
              <path d="M253 206 L342 261 M237 246 L337 293 M267 308 L345 333 M463 246 L552 203 M466 291 L548 257 M462 336 L538 316" />
              <path d="M303 405 L362 438 M468 393 L526 374 M343 491 L397 522 M459 478 L502 449" />
            </g>
          </g>

          <path className="island-coastline" d={LA_PALMA_PATH} />

          <g className="contour-lines" aria-hidden="true">
            <path d="M292 133 C332 91 421 78 493 108 C547 130 563 176 533 216 C500 258 429 275 362 257 C303 241 270 189 292 133 Z" />
            <path d="M315 156 C352 124 415 119 465 139 C504 155 516 184 494 213 C469 243 417 250 371 237 C332 226 299 193 315 156 Z" />
            <path d="M313 303 C353 279 424 282 475 309 C516 331 527 365 503 389 C476 415 421 419 370 399 C328 383 296 337 313 303 Z" />
            <path d="M336 391 C371 370 428 376 467 403 C498 425 505 457 484 478 C458 504 416 500 380 480 C346 461 319 421 336 391 Z" />
            <path d="M367 493 C394 475 440 482 470 509 C496 532 495 563 476 583 C452 607 419 599 394 579 C370 560 350 516 367 493 Z" />
          </g>

          <g className="road-network" aria-label="Simplified island access routes">
            <path d="M277 270 C305 298 330 330 365 356 C397 381 427 419 438 500 C445 548 440 588 427 624" />
            <path d="M365 356 C407 344 454 333 511 320 C541 313 553 291 557 260" />
            <path d="M278 274 C307 246 337 232 365 225 C400 217 432 223 477 246 C510 264 528 289 511 320" />
            <path d="M328 345 C345 331 356 298 365 225" />
          </g>

          <g className="map-place-labels" aria-hidden="true">
            <text x="242" y="252">TIJARAFE</text>
            <text x="276" y="341">LOS LLANOS</text>
            <text x="481" y="308">S/C DE LA PALMA</text>
            <text x="406" y="591">FUENCALIENTE</text>
            <g className="summit-label" transform="translate(374 192)">
              <path d="M0 -6 L6 5 L-6 5 Z" />
              <text x="11" y="-2">ROQUE DE LOS MUCHACHOS</text>
              <text x="11" y="9" className="map-place-labels__sub">2,426 m</text>
            </g>
          </g>

          <g className="spread-model" key={`${scenario?.id ?? 'none'}-${scenario?.riskScore ?? 0}`}>
            {scenario?.rings.slice().reverse().map((ring, index) => (
              <ellipse
                key={ring.minute}
                className={`spread-ring spread-ring--${index}`}
                cx={ring.centerX}
                cy={ring.centerY}
                rx={ring.radiusX}
                ry={ring.radiusY}
                pathLength="100"
                transform={`rotate(${ring.rotation} ${ring.centerX} ${ring.centerY})`}
              />
            ))}
            <g className="spread-vector" transform={`rotate(${WIND_MAP[scenario?.windPreset ?? 'observed'].rotation} ${FIRE_ORIGIN.x} ${FIRE_ORIGIN.y})`}>
              <path d="M394 390 C429 384 465 371 505 346" />
              <circle cx="505" cy="346" r="3" />
            </g>
          </g>

          <g className="smoke-plume" transform={`rotate(${WIND_MAP[scenario?.windPreset ?? 'observed'].rotation * .35} ${FIRE_ORIGIN.x} ${FIRE_ORIGIN.y})`} aria-hidden="true">
            <path className="smoke smoke--1" d="M391 380 C378 362 389 348 376 331 C364 315 372 300 362 286" pathLength="100" />
            <path className="smoke smoke--2" d="M400 381 C412 360 397 347 410 329 C422 313 412 299 420 284" pathLength="100" />
            <path className="smoke smoke--3" d="M396 379 C392 360 404 349 398 335 C391 319 401 310 397 296" pathLength="100" />
          </g>

          <g className="ember-field" aria-hidden="true">
            <circle className="ember ember--1" cx="390" cy="377" r="1.6" />
            <circle className="ember ember--2" cx="397" cy="373" r="1.2" />
            <circle className="ember ember--3" cx="403" cy="379" r="1.4" />
            <circle className="ember ember--4" cx="387" cy="384" r="1" />
            <circle className="ember ember--5" cx="407" cy="385" r="1.2" />
            <circle className="ember ember--6" cx="400" cy="368" r=".9" />
          </g>

          <g className="ignition-marker" transform={`translate(${FIRE_ORIGIN.x} ${FIRE_ORIGIN.y})`} aria-label="Animated synthetic exercise ignition">
            <circle r="33" className="ignition-marker__glow" filter="url(#glow)" />
            <circle r="17" className="ignition-marker__pulse" />
            <g className="flame-stack" aria-hidden="true">
              <path className="flame flame--back" d="M-9 9 C-15 -1 -8 -10 -2 -19 C0 -10 6 -8 5 -1 C11 -8 15 -2 13 5 C11 13 4 17 -3 16 C-8 15 -11 13 -9 9 Z" />
              <path className="flame flame--mid" d="M-4 10 C-9 2 -3 -4 1 -12 C2 -5 8 -3 7 4 C10 1 11 8 7 12 C3 16 -2 15 -4 10 Z" />
              <path className="flame flame--core" d="M0 11 C-3 6 1 2 3 -3 C4 2 8 5 6 10 C5 14 1 15 0 11 Z" />
            </g>
            <circle r="6.5" fill="url(#fireCore)" opacity=".64" />
            <circle r="22" className="ignition-marker__ring" />
          </g>

          <g className="wind-arrow" transform="translate(625 122)">
            <circle r="41" />
            <path d="M-21 6 L21 -8 M13 -15 L21 -8 L14 0" transform={`rotate(${WIND_MAP[scenario?.windPreset ?? 'observed'].rotation})`} />
            <text x="0" y="56">{WIND_MAP[scenario?.windPreset ?? 'observed'].label}</text>
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

          <g className="scale-bar" transform="translate(625 630)" aria-hidden="true">
            <path d="M0 0 H80 M0 -4 V4 M40 -4 V4 M80 -4 V4" />
            <text x="40" y="16">≈ 10 km</text>
          </g>
        </svg>

        <div className="map-legend">
          <span><i className="legend-fire" /> exercise origin</span>
          <span><i className="legend-contour" /> modeled attention area</span>
          <span><i className="legend-zone" /> sector</span>
          <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noreferrer">© OpenStreetMap contributors · coastline</a>
          <span className="map-legend__truth"><Check size={12} /> all data is synthetic</span>
        </div>
        <div className="map-tools" aria-hidden="true"><button><Compass size={16} /></button><button><Layers3 size={16} /></button></div>
      </div>
    </section>
  )
}
