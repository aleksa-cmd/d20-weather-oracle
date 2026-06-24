import streamlit as st
import requests
import random

st.set_page_config(page_title="D20 Weather Oracle", page_icon="🎲", layout="centered")

CITIES = [
    {"name": "Reykjavik",       "lat": 64.1355,  "lon": -21.8954},
    {"name": "Oslo",            "lat": 59.9139,  "lon": 10.7522},
    {"name": "Stockholm",       "lat": 59.3293,  "lon": 18.0686},
    {"name": "Helsinki",        "lat": 60.1699,  "lon": 24.9384},
    {"name": "Copenhagen",      "lat": 55.6761,  "lon": 12.5683},
    {"name": "Edinburgh",       "lat": 55.9533,  "lon": -3.1883},
    {"name": "Dublin",          "lat": 53.3498,  "lon": -6.2603},
    {"name": "London",          "lat": 51.5074,  "lon": -0.1278},
    {"name": "Amsterdam",       "lat": 52.3676,  "lon": 4.9041},
    {"name": "Brussels",        "lat": 50.8503,  "lon": 4.3517},
    {"name": "Paris",           "lat": 48.8566,  "lon": 2.3522},
    {"name": "Berlin",          "lat": 52.5200,  "lon": 13.4050},
    {"name": "Warsaw",          "lat": 52.2297,  "lon": 21.0122},
    {"name": "Vienna",          "lat": 48.2082,  "lon": 16.3738},
    {"name": "Zurich",          "lat": 47.3769,  "lon": 8.5417},
    {"name": "Milan",           "lat": 45.4642,  "lon": 9.1900},
    {"name": "Rome",            "lat": 41.9028,  "lon": 12.4964},
    {"name": "Barcelona",       "lat": 41.3851,  "lon": 2.1734},
    {"name": "Madrid",          "lat": 40.4168,  "lon": -3.7038},
    {"name": "Lisbon",          "lat": 38.7223,  "lon": -9.1393},
    {"name": "Athens",          "lat": 37.9838,  "lon": 23.7275},
    {"name": "Istanbul",        "lat": 41.0082,  "lon": 28.9784},
    {"name": "Kyiv",            "lat": 50.4501,  "lon": 30.5234},
    {"name": "Moscow",          "lat": 55.7558,  "lon": 37.6173},
    {"name": "Bucharest",       "lat": 44.4268,  "lon": 26.1025},
    {"name": "Sofia",           "lat": 42.6977,  "lon": 23.3219},
    {"name": "Belgrade",        "lat": 44.7866,  "lon": 20.4489},
    {"name": "Budapest",        "lat": 47.4979,  "lon": 19.0402},
    {"name": "Prague",          "lat": 50.0755,  "lon": 14.4378},
    {"name": "Riga",            "lat": 56.9496,  "lon": 24.1052},
    {"name": "Tallinn",         "lat": 59.4370,  "lon": 24.7536},
    {"name": "Cairo",           "lat": 30.0444,  "lon": 31.2357},
    {"name": "Nairobi",         "lat": -1.2921,  "lon": 36.8219},
    {"name": "Lagos",           "lat": 6.5244,   "lon": 3.3792},
    {"name": "Casablanca",      "lat": 33.5731,  "lon": -7.5898},
    {"name": "Johannesburg",    "lat": -26.2041, "lon": 28.0473},
    {"name": "Accra",           "lat": 5.6037,   "lon": -0.1870},
    {"name": "Dakar",           "lat": 14.7167,  "lon": -17.4677},
    {"name": "Algiers",         "lat": 36.7538,  "lon": 3.0588},
    {"name": "Khartoum",        "lat": 15.5007,  "lon": 32.5599},
    {"name": "Dubai",           "lat": 25.2048,  "lon": 55.2708},
    {"name": "Riyadh",          "lat": 24.7136,  "lon": 46.6753},
    {"name": "Baghdad",         "lat": 33.3152,  "lon": 44.3661},
    {"name": "Tehran",          "lat": 35.6892,  "lon": 51.3890},
    {"name": "Karachi",         "lat": 24.8607,  "lon": 67.0011},
    {"name": "Mumbai",          "lat": 19.0760,  "lon": 72.8777},
    {"name": "New Delhi",       "lat": 28.6139,  "lon": 77.2090},
    {"name": "Bangkok",         "lat": 13.7563,  "lon": 100.5018},
    {"name": "Ho Chi Minh City","lat": 10.8231,  "lon": 106.6297},
    {"name": "Singapore",       "lat": 1.3521,   "lon": 103.8198},
    {"name": "Jakarta",         "lat": -6.2088,  "lon": 106.8456},
    {"name": "Manila",          "lat": 14.5995,  "lon": 120.9842},
    {"name": "Hong Kong",       "lat": 22.3193,  "lon": 114.1694},
    {"name": "Seoul",           "lat": 37.5665,  "lon": 126.9780},
    {"name": "Tokyo",           "lat": 35.6762,  "lon": 139.6503},
    {"name": "Beijing",         "lat": 39.9042,  "lon": 116.4074},
    {"name": "Shanghai",        "lat": 31.2304,  "lon": 121.4737},
    {"name": "Sydney",          "lat": -33.8688, "lon": 151.2093},
    {"name": "Melbourne",       "lat": -37.8136, "lon": 144.9631},
    {"name": "Auckland",        "lat": -36.8485, "lon": 174.7633},
    {"name": "Honolulu",        "lat": 21.3069,  "lon": -157.8583},
    {"name": "Anchorage",       "lat": 61.2181,  "lon": -149.9003},
    {"name": "Vancouver",       "lat": 49.2827,  "lon": -123.1207},
    {"name": "San Francisco",   "lat": 37.7749,  "lon": -122.4194},
    {"name": "Los Angeles",     "lat": 34.0522,  "lon": -118.2437},
    {"name": "Chicago",         "lat": 41.8781,  "lon": -87.6298},
    {"name": "Miami",           "lat": 25.7617,  "lon": -80.1918},
    {"name": "New York",        "lat": 40.7128,  "lon": -74.0060},
    {"name": "Toronto",         "lat": 43.6532,  "lon": -79.3832},
    {"name": "Mexico City",     "lat": 19.4326,  "lon": -99.1332},
    {"name": "Bogota",          "lat": 4.7110,   "lon": -74.0721},
    {"name": "Lima",            "lat": -12.0464, "lon": -77.0428},
    {"name": "Santiago",        "lat": -33.4489, "lon": -70.6693},
    {"name": "Buenos Aires",    "lat": -34.6037, "lon": -58.3816},
    {"name": "Sao Paulo",       "lat": -23.5505, "lon": -46.6333},
    {"name": "Rio de Janeiro",  "lat": -22.9068, "lon": -43.1729},
    {"name": "Quito",           "lat": -0.1807,  "lon": -78.4678},
    {"name": "Montevideo",      "lat": -34.9011, "lon": -56.1645},
    {"name": "Tbilisi",         "lat": 41.6941,  "lon": 44.8337},
    {"name": "Amman",           "lat": 31.9454,  "lon": 35.9284},
    {"name": "Tel Aviv",        "lat": 32.0853,  "lon": 34.7818},
    {"name": "Muscat",          "lat": 23.5880,  "lon": 58.3829},
    {"name": "Doha",            "lat": 25.2854,  "lon": 51.5310},
    {"name": "Ankara",          "lat": 39.9334,  "lon": 32.8597},
    {"name": "Colombo",         "lat": 6.9271,   "lon": 79.8612},
    {"name": "Ulaanbaatar",     "lat": 47.8864,  "lon": 106.9057},
    {"name": "Almaty",          "lat": 43.2220,  "lon": 76.8512},
    {"name": "Addis Ababa",     "lat": 8.9806,   "lon": 38.7578},
    {"name": "Tunis",           "lat": 36.8065,  "lon": 10.1815},
    {"name": "Havana",          "lat": 23.1136,  "lon": -82.3666},
    {"name": "Caracas",         "lat": 10.4806,  "lon": -66.9036},
]


def get_temperatures(cities):
    batch_size = 50
    results = []
    for i in range(0, len(cities), batch_size):
        batch = cities[i : i + batch_size]
        lats = ",".join(str(c["lat"]) for c in batch)
        lons = ",".join(str(c["lon"]) for c in batch)
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={"latitude": lats, "longitude": lons, "current_weather": "true"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        if isinstance(data, dict):
            data = [data]
        for j, item in enumerate(data):
            if j >= len(batch):
                break
            cw = item.get("current_weather", {})
            if "temperature" in cw:
                results.append({"name": batch[j]["name"], "temp": cw["temperature"]})
    return results


def find_cities(target_temp):
    all_cities = get_temperatures(CITIES)
    all_cities.sort(key=lambda x: abs(x["temp"] - target_temp))
    return [
        {**c, "diff": round(abs(c["temp"] - target_temp), 1)}
        for c in all_cities[:2]
    ]


# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  .main { background: #0a0f1e; }
  .block-container { max-width: 560px; }
  h1 { text-align: center; }
  .city-card {
    background: #1e293b; border: 1px solid #334155;
    border-radius: 0.75rem; padding: 1rem 1.5rem;
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 0.5rem;
  }
  .city-card-name { font-size: 1.1rem; font-weight: 600; color: #f1f5f9; }
  .city-card-sub  { font-size: 0.8rem; color: #64748b; }
  .city-card-temp { font-size: 1.4rem; font-weight: 700; color: #facc15; }
</style>
""", unsafe_allow_html=True)

# ── Title ──────────────────────────────────────────────────────────────────────
st.markdown("# 🎲 D20 Weather Oracle")
st.markdown(
    "<p style='text-align:center; color:#475569;'>Roll the dice · find a city · discover the world</p>",
    unsafe_allow_html=True,
)
st.divider()

# ── Dice section ───────────────────────────────────────────────────────────────
if "roll_result" not in st.session_state:
    st.session_state.roll_result = None
if "roll_key" not in st.session_state:
    st.session_state.roll_key = 0

result_val = st.session_state.roll_result if st.session_state.roll_result else 0
roll_key   = st.session_state.roll_key

DICE_3D = f"""<!DOCTYPE html>
<html>
<head>
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:100%;height:100%;background:#0a0f1e;overflow:hidden}}
  #wrap{{position:relative;width:100%;height:100%}}
  canvas{{display:block;width:100%!important;height:100%!important}}
  #num{{
    position:absolute;top:42%;left:50%;
    transform:translate(-50%,-50%) scale(0.2);
    opacity:0;
    transition:opacity 0.7s ease, transform 0.7s cubic-bezier(.34,1.56,.64,1);
    font:bold 88px Georgia,serif;
    color:#facc15;
    text-shadow:0 0 25px rgba(250,204,21,1),0 0 60px rgba(250,204,21,0.5);
    pointer-events:none;user-select:none;
  }}
  #num.show{{opacity:1;transform:translate(-50%,-50%) scale(1)}}
  #label{{
    position:absolute;bottom:8px;left:50%;
    transform:translateX(-50%);
    font:13px/1 sans-serif;letter-spacing:.12em;
    color:#475569;pointer-events:none;user-select:none;
  }}
</style>
</head>
<body>
<div id="wrap">
  <canvas id="c"></canvas>
  <div id="num"></div>
  <div id="label">d20</div>
</div>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script>
(function(){{
  const RESULT   = {result_val};
  const ROLL_KEY = {roll_key};   // changes each roll → forces remount
  const ANIMATE  = RESULT > 0;

  const W = window.innerWidth, H = window.innerHeight;
  const scene    = new THREE.Scene();
  const camera   = new THREE.PerspectiveCamera(52, W/H, 0.1, 100);
  camera.position.z = 5.8;

  const renderer = new THREE.WebGLRenderer({{canvas:document.getElementById('c'),antialias:true,alpha:true}});
  renderer.setSize(W, H);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
  renderer.setClearColor(0x0a0f1e, 1);

  // ── Lights ──────────────────────────────────────────────────────────────────
  scene.add(new THREE.AmbientLight(0x223366, 4));
  const key = new THREE.PointLight(0xffd060, 5, 40);
  key.position.set(5, 6, 5);
  scene.add(key);
  const fill = new THREE.PointLight(0x4466ff, 2.5, 30);
  fill.position.set(-5, -3, -4);
  scene.add(fill);
  const rim = new THREE.PointLight(0xffffff, 1.5, 20);
  rim.position.set(0, -6, 2);
  scene.add(rim);

  // ── Icosahedron ─────────────────────────────────────────────────────────────
  const geo = new THREE.IcosahedronGeometry(2, 0);
  const mat = new THREE.MeshPhongMaterial({{
    color:     0x0e2060,
    emissive:  0x040e30,
    specular:  0x99aaff,
    shininess: 140,
    transparent: true,
    opacity: 0.93
  }});
  const mesh = new THREE.Mesh(geo, mat);
  scene.add(mesh);

  // Gold edges
  const edgeGeo = new THREE.EdgesGeometry(geo);
  const edgeMat = new THREE.LineBasicMaterial({{color:0xfacc15, linewidth:1}});
  mesh.add(new THREE.LineSegments(edgeGeo, edgeMat));

  // Inner dimmer edges for depth
  const innerGeo = new THREE.EdgesGeometry(new THREE.IcosahedronGeometry(1.65, 0));
  const innerMat = new THREE.LineBasicMaterial({{color:0xfacc1530, linewidth:1}});
  const innerEdges = new THREE.LineSegments(innerGeo, innerMat);
  mesh.add(innerEdges);

  // ── Animation state ─────────────────────────────────────────────────────────
  const TOTAL = 160;
  let frame = 0;
  let done  = !ANIMATE;

  // Random tumble axes
  const vx = (ANIMATE ? 1 : 0) * (0.10 + Math.random()*0.08);
  const vy = (ANIMATE ? 1 : 0) * (0.13 + Math.random()*0.10);
  const vz = (ANIMATE ? 1 : 0) * (Math.random()-0.5)*0.06;

  // Ease-out cubic
  function easeOut(t){{ return 1 - Math.pow(1-t, 3); }}

  const numEl = document.getElementById('num');

  // If no roll yet, show idle state
  if(!ANIMATE){{
    numEl.textContent = '?';
    numEl.style.opacity = '0.35';
    numEl.style.transform = 'translate(-50%,-50%) scale(0.7)';
  }}

  function tick(){{
    requestAnimationFrame(tick);

    if(!done){{
      const t     = Math.min(frame / TOTAL, 1);
      const speed = 1 - easeOut(t);
      mesh.rotation.x += vx * speed;
      mesh.rotation.y += vy * speed;
      mesh.rotation.z += vz * speed;
      frame++;

      // Pulse the edge colour while spinning
      const pulse = 0.6 + 0.4*Math.sin(frame * 0.18);
      edgeMat.color.setRGB(pulse, pulse * 0.8, 0);

      if(frame >= TOTAL){{
        done = true;
        edgeMat.color.set(0xfacc15);
        numEl.textContent = RESULT;
        numEl.classList.add('show');
        // Intensify key light on landing
        key.intensity = 8;
        setTimeout(()=>{{ key.intensity = 5; }}, 600);
      }}
    }} else if(ANIMATE){{
      // Slow idle spin after landing
      mesh.rotation.y += 0.004;
    }}

    renderer.render(scene, camera);
  }}
  tick();
}})();
</script>
</body>
</html>"""

st.components.v1.html(DICE_3D, height=320)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    label = "Roll Again" if st.session_state.roll_result else "Roll d20"
    if st.button(label, use_container_width=True, type="primary"):
        st.session_state.roll_result = random.randint(1, 20)
        st.session_state.roll_key   += 1
        st.rerun()

if st.session_state.roll_result:
    st.markdown(
        f"<p style='text-align:center; color:#94a3b8; font-size:1rem; margin-top:0.25rem;'>"
        f"You rolled <strong style='color:#facc15; font-size:1.3rem;'>"
        f"{st.session_state.roll_result}</strong></p>",
        unsafe_allow_html=True,
    )

st.divider()

# ── Weather search section ─────────────────────────────────────────────────────
st.subheader("Weather Oracle")

default_val = st.session_state.roll_result if st.session_state.roll_result else 1
dice_input = st.number_input(
    "Enter dice roll (1–20)",
    min_value=1,
    max_value=20,
    value=default_val,
    step=1,
    help="Type the number you rolled (or any 1–20) and press Enter or click Search",
)

target_temp = int(dice_input) * 2
st.markdown(
    f"<p style='color:#64748b; font-size:0.9rem;'>"
    f"{int(dice_input)} × 2 = "
    f"<strong style='color:#38bdf8;'>{target_temp}°C</strong>"
    f" — searching for cities at this temperature…</p>",
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns([1, 2, 1])
with col_b:
    search_clicked = st.button("Search Cities", use_container_width=True)

if search_clicked:
    with st.spinner(f"Querying {len(CITIES)} cities via Open-Meteo…"):
        try:
            cities = find_cities(target_temp)
            st.markdown(
                f"<p style='color:#64748b; font-size:0.85rem; margin-bottom:0.5rem;'>"
                f"Cities nearest to {target_temp}°C right now:</p>",
                unsafe_allow_html=True,
            )
            if not cities:
                st.info("No cities found close to that temperature. Try a different value.")
            else:
                for c in cities:
                    st.markdown(
                        f"""
                        <div class="city-card">
                          <div>
                            <div class="city-card-name">{c['name']}</div>
                            <div class="city-card-sub">±{c['diff']}°C from {target_temp}°C</div>
                          </div>
                          <div class="city-card-temp">{c['temp']}°C</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        except Exception as e:
            st.error(f"Could not reach Open-Meteo API: {e}")

st.divider()
st.markdown(
    "<p style='text-align:center; color:#1e293b; font-size:0.75rem;'>"
    "Powered by Open-Meteo · No API key required</p>",
    unsafe_allow_html=True,
)
