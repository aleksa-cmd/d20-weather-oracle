import { useEffect, useRef, useState, useCallback } from 'react'
import * as THREE from 'three'
import './DiceRoller.css'

export default function DiceRoller({ onRoll }) {
  const mountRef = useRef(null)
  const threeRef = useRef(null)
  const rollRef  = useRef({ active: false, frame: 0, total: 160, vx: 0, vy: 0, vz: 0, onDone: null })
  const [isRolling, setIsRolling] = useState(false)
  const [result,    setResult]    = useState(null)
  const [showNum,   setShowNum]   = useState(false)

  useEffect(() => {
    const container = mountRef.current
    const W = container.offsetWidth || 480
    const H = 320

    // ── Scene / camera ─────────────────────────────────────────────────────
    const scene  = new THREE.Scene()
    const camera = new THREE.PerspectiveCamera(52, W / H, 0.1, 100)
    camera.position.z = 5.8

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true })
    renderer.setSize(W, H)
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setClearColor(0x0a0f1e, 1)
    // Use ACES tone-mapping for nicer output with physically correct lights
    renderer.toneMapping        = THREE.ACESFilmicToneMapping
    renderer.toneMappingExposure = 1.2
    container.appendChild(renderer.domElement)

    // ── Lights (r155+ physically correct — intensities in candelas) ────────
    scene.add(new THREE.AmbientLight(0x223366, 2))

    const keyLight = new THREE.PointLight(0xffd060, 150, 40)
    keyLight.position.set(5, 6, 5)          // ← must use .set(), not Object.assign
    scene.add(keyLight)

    const fillLight = new THREE.PointLight(0x4466ff, 80, 30)
    fillLight.position.set(-5, -3, -4)
    scene.add(fillLight)

    const rimLight = new THREE.PointLight(0xffffff, 60, 20)
    rimLight.position.set(0, -6, 2)
    scene.add(rimLight)

    // ── D20 (icosahedron) — MeshStandardMaterial for PBR lights ───────────
    const geo = new THREE.IcosahedronGeometry(2, 0)
    const mat = new THREE.MeshStandardMaterial({
      color:       0x0e2060,
      emissive:    0x040e30,
      roughness:   0.25,
      metalness:   0.70,
      transparent: true,
      opacity:     0.93,
    })
    const mesh = new THREE.Mesh(geo, mat)
    scene.add(mesh)

    // Gold outer edges
    const edgeMat = new THREE.LineBasicMaterial({ color: 0xfacc15 })
    mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(geo), edgeMat))

    // Dim inner edges for depth
    mesh.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.65, 0)),
      new THREE.LineBasicMaterial({ color: 0x1a3070 })
    ))

    threeRef.current = { renderer, mesh, edgeMat, keyLight }

    // ── Animation loop ─────────────────────────────────────────────────────
    let animId
    const easeOut = t => 1 - Math.pow(1 - t, 3)

    const tick = () => {
      animId = requestAnimationFrame(tick)
      const rs = rollRef.current

      if (rs.active) {
        const t     = Math.min(rs.frame / rs.total, 1)
        const speed = 1 - easeOut(t)
        mesh.rotation.x += rs.vx * speed
        mesh.rotation.y += rs.vy * speed
        mesh.rotation.z += rs.vz * speed

        // Pulse edges orange→gold while rolling
        const p = 0.6 + 0.4 * Math.sin(rs.frame * 0.18)
        edgeMat.color.setRGB(p, p * 0.8, 0)

        rs.frame++
        if (rs.frame >= rs.total) {
          rs.active = false
          edgeMat.color.set(0xfacc15)
          keyLight.intensity = 220
          setTimeout(() => { keyLight.intensity = 150 }, 600)
          rs.onDone?.()
        }
      } else {
        mesh.rotation.y += 0.004   // idle spin
      }

      renderer.render(scene, camera)
    }
    tick()

    return () => {
      cancelAnimationFrame(animId)
      if (container.contains(renderer.domElement)) container.removeChild(renderer.domElement)
      renderer.dispose()
    }
  }, [])

  const roll = useCallback(() => {
    if (rollRef.current.active) return
    const final = Math.floor(Math.random() * 20) + 1
    setIsRolling(true)
    setResult(null)
    setShowNum(false)

    rollRef.current = {
      active: true,
      frame:  0,
      total:  160,
      vx:  0.10 + Math.random() * 0.08,
      vy:  0.13 + Math.random() * 0.10,
      vz: (Math.random() - 0.5) * 0.06,
      onDone: () => {
        setResult(final)
        setIsRolling(false)
        setShowNum(true)
        onRoll?.(final)
      },
    }
  }, [onRoll])

  return (
    <div className="dice-roller">
      <div className="dice-stage">
        <div ref={mountRef} className="dice-canvas" />
        <div className={`dice-num ${showNum ? 'show' : ''} ${!result && !isRolling ? 'idle' : ''}`}>
          {isRolling ? '' : (result ?? '?')}
        </div>
        <div className="dice-label-bottom">d20</div>
      </div>

      <button className="roll-btn" onClick={roll} disabled={isRolling}>
        {isRolling ? 'Rolling…' : result !== null ? 'Roll Again' : 'Roll d20'}
      </button>

      {result !== null && !isRolling && (
        <p className="roll-result">You rolled <strong>{result}</strong></p>
      )}
    </div>
  )
}
