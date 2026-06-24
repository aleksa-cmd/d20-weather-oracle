import { useState } from 'react'
import DiceRoller from './components/DiceRoller'
import WeatherSearch from './components/WeatherSearch'
import './App.css'

export default function App() {
  const [lastRoll, setLastRoll] = useState(null)

  return (
    <>
      <header className="app-header">
        <h1 className="app-title">D20 Weather Oracle</h1>
        <p className="app-subtitle">Roll the dice · find a city · discover the world</p>
      </header>

      <main className="main-card">
        <DiceRoller onRoll={setLastRoll} />
        <div className="divider" />
        <WeatherSearch suggestedValue={lastRoll} />
      </main>

      <footer className="footer">
        Powered by Open-Meteo · No API key required
      </footer>
    </>
  )
}
