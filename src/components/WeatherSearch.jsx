import { useState } from 'react'
import './WeatherSearch.css'

export default function WeatherSearch({ suggestedValue }) {
  const [inputVal, setInputVal] = useState(suggestedValue ?? '')
  const [loading, setLoading] = useState(false)
  const [matches, setMatches] = useState(null)
  const [error, setError] = useState(null)
  const [searchedTemp, setSearchedTemp] = useState(null)

  const parsed = parseInt(inputVal, 10)
  const targetTemp = !isNaN(parsed) && parsed >= 1 && parsed <= 20 ? parsed * 2 : null

  async function search() {
    if (targetTemp === null) return
    setLoading(true)
    setError(null)
    setMatches(null)
    setSearchedTemp(targetTemp)

    try {
      const res = await fetch(`/api/weather?temp=${targetTemp}`)
      if (!res.ok) throw new Error(`Server error ${res.status}`)
      const data = await res.json()
      setMatches(data.matches ?? [])
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') search()
  }

  return (
    <div className="weather-search">
      <h2>Weather Oracle</h2>

      <div className="input-row">
        <input
          className="dice-input"
          type="number"
          min="1"
          max="20"
          placeholder="Enter dice roll (1–20)"
          value={inputVal}
          onChange={e => setInputVal(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button
          className="search-btn"
          onClick={search}
          disabled={targetTemp === null || loading}
        >
          {loading ? <span className="spinner" /> : 'Search'}
        </button>
      </div>

      {targetTemp !== null && (
        <p className="calc-display">
          {parsed} × 2 = <span>{targetTemp}°C</span> — finding cities at this temperature…
        </p>
      )}

      {error && <p className="error-msg">Error: {error}</p>}

      {matches !== null && !loading && (
        <div className="results-card">
          <div className="results-header">
            Cities near {searchedTemp}°C right now
          </div>
          {matches.length === 0 ? (
            <p className="no-matches">No cities found within 2°C of {searchedTemp}°C</p>
          ) : (
            matches.map(city => (
              <div key={city.name} className="city-row">
                <div>
                  <div className="city-name">{city.name}</div>
                  <div className="city-diff">±{city.diff}°C from target</div>
                </div>
                <div className="city-temp">{city.temp}°C</div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  )
}
