import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it } from 'vitest'
import { incidentStore } from '../store/incidentStore'
import { App } from './App'

describe('incident twin app', () => {
  beforeEach(() => incidentStore.getState().resetExercise())
  afterEach(cleanup)

  it('presents synthetic provenance and keeps final approval in the human UI', () => {
    render(<App />)

    expect(screen.getAllByText('SYNTHETIC EXERCISE').length).toBeGreaterThan(0)
    expect(screen.getByRole('img', { name: /synthetic exercise map/i })).toBeInTheDocument()

    const stageButtons = screen.getAllByRole('button', { name: /stage for review/i })
    fireEvent.click(stageButtons.at(-1)!)
    expect(screen.getByText('Agent proposal staged')).toBeInTheDocument()

    fireEvent.click(screen.getByRole('button', { name: /approve exercise plan/i }))
    expect(screen.getByText('Human-approved exercise plan')).toBeInTheDocument()
    expect(screen.getByText(/final approval is deliberately not exposed/i)).toBeInTheDocument()
  })

  it('explains the complementary human and agent workflow in the interface', () => {
    render(<App />)

    fireEvent.click(screen.getByRole('button', { name: /how it works/i }))

    expect(screen.getByText(/rehearse decisions on one shared map/i)).toBeInTheDocument()
    expect(screen.getByText('Human grounds')).toBeInTheDocument()
    expect(screen.getByText('Agent rehearses')).toBeInTheDocument()
    expect(screen.getByText('Human decides')).toBeInTheDocument()
    expect(screen.getByText(/blocked-road exercise note/i)).toBeInTheDocument()
  })
})
