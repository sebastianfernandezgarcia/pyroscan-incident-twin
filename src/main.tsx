import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { App } from './app/App'
import './app/App.css'
import { startIncidentTools } from './webmcp/registerIncidentTools'

const siteTools = startIncidentTools()
window.addEventListener('pagehide', () => siteTools.controller.abort(), { once: true })

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
