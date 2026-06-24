import { useState, useEffect } from 'react'
import './WeatherSearch.css'

export default function WeatherSearch({ diceRoll }) {
  const [loading, setLoading]         = useState(false)
  const [matches, setMatches]         = useState(null)
  const [error, setError]             = useState(null)
  const [searchedTemp, setSearchedTemp] = useState(null)

  const targetTemp = diceRoll ? diceRoll * 2 : null

  useEffect(() => {
    if (!targetTemp) return
    setLoading(true)
    setError(null)
    setMatches(null)
    setSearchedTemp(targetTemp)

    fetch(`/api/weather?temp=${targetTemp}`)
      .then(r => {
        if (!r.ok) throw new Error(`Server error ${r.status}`)
        return r.json()
      })
      .then(data => setMatches(data.matches ?? []))
      .catch(e => setError(e.message))
      .finally(() => setLoading(false))
  }, [diceRoll])

  if (!diceRoll) {
    return (
      <div className="weather-idle">
        <p>Roll the dice to find your city</p>
      </div>
    )
  }

  return (
    <div className="weather-search">
      <div className="calc-display">
        {diceRoll} × 2 = <span>{targetTemp}°C</span>
        <span className="calc-sub"> — searching cities at this temperature</span>
      </div>

      {loading && (
        <div className="spinner-wrap">
          <div className="spinner" />
          <span>Querying world cities…</span>
        </div>
      )}

      {error && <p className="error-msg">Error: {error}</p>}

      {matches !== null && !loading && (
        <div className="results-card">
          <div className="results-header">
            Cities near {searchedTemp}°C right now
          </div>
          {matches.length === 0 ? (
            <p className="no-matches">No cities found near {searchedTemp}°C</p>
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
