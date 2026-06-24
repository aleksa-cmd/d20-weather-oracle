import { useState, useRef } from 'react'
import './DiceRoller.css'

export default function DiceRoller({ onRoll }) {
  const [rolling, setRolling] = useState(false)
  const [result, setResult] = useState(null)
  const [display, setDisplay] = useState('?')
  const timerRef = useRef(null)

  function roll() {
    if (rolling) return
    const final = Math.floor(Math.random() * 20) + 1
    setRolling(true)
    setResult(null)

    let elapsed = 0

    function tick(delay) {
      elapsed += delay
      setDisplay(Math.floor(Math.random() * 20) + 1)

      if (elapsed >= 2000) {
        setDisplay(final)
        setResult(final)
        setRolling(false)
        if (onRoll) onRoll(final)
        return
      }

      const next =
        elapsed < 600 ? 50 :
        elapsed < 1000 ? 80 :
        elapsed < 1500 ? 130 : 220

      timerRef.current = setTimeout(() => tick(next), next)
    }

    timerRef.current = setTimeout(() => tick(50), 50)
  }

  const wrapperClass = `d20-wrapper${rolling ? ' rolling' : ''}${result && !rolling ? ' landed' : ''}`

  return (
    <div className="dice-roller">
      <div className={wrapperClass}>
        <svg className="d20-svg" viewBox="0 0 200 200">
          {/* D20 pentagon shape */}
          <polygon
            className="d20-face"
            points="100,8 192,72 159,178 41,178 8,72"
          />
          {/* Inner decorative lines (d20 feel) */}
          <polygon
            fill="none"
            stroke="#facc1540"
            strokeWidth="1"
            points="100,30 172,82 148,158 52,158 28,82"
          />
          <text className="d20-number" x="100" y="105">{display}</text>
          <text className="dice-label" x="100" y="150">d20</text>
        </svg>
      </div>

      <button className="roll-btn" onClick={roll} disabled={rolling}>
        {rolling ? 'Rolling…' : result !== null ? 'Roll Again' : 'Roll d20'}
      </button>

      {result !== null && !rolling && (
        <p className="roll-result">
          You rolled <strong>{result}</strong>
        </p>
      )}
    </div>
  )
}
