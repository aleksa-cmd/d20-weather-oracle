from flask import Flask, request, jsonify
import requests as http

app = Flask(__name__)

CITIES = [
    {"name": "Reykjavik", "lat": 64.1355, "lon": -21.8954},
    {"name": "Oslo", "lat": 59.9139, "lon": 10.7522},
    {"name": "Stockholm", "lat": 59.3293, "lon": 18.0686},
    {"name": "Helsinki", "lat": 60.1699, "lon": 24.9384},
    {"name": "Copenhagen", "lat": 55.6761, "lon": 12.5683},
    {"name": "Edinburgh", "lat": 55.9533, "lon": -3.1883},
    {"name": "Dublin", "lat": 53.3498, "lon": -6.2603},
    {"name": "London", "lat": 51.5074, "lon": -0.1278},
    {"name": "Amsterdam", "lat": 52.3676, "lon": 4.9041},
    {"name": "Brussels", "lat": 50.8503, "lon": 4.3517},
    {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
    {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
    {"name": "Warsaw", "lat": 52.2297, "lon": 21.0122},
    {"name": "Vienna", "lat": 48.2082, "lon": 16.3738},
    {"name": "Zurich", "lat": 47.3769, "lon": 8.5417},
    {"name": "Milan", "lat": 45.4642, "lon": 9.1900},
    {"name": "Rome", "lat": 41.9028, "lon": 12.4964},
    {"name": "Barcelona", "lat": 41.3851, "lon": 2.1734},
    {"name": "Madrid", "lat": 40.4168, "lon": -3.7038},
    {"name": "Lisbon", "lat": 38.7223, "lon": -9.1393},
    {"name": "Athens", "lat": 37.9838, "lon": 23.7275},
    {"name": "Istanbul", "lat": 41.0082, "lon": 28.9784},
    {"name": "Kyiv", "lat": 50.4501, "lon": 30.5234},
    {"name": "Moscow", "lat": 55.7558, "lon": 37.6173},
    {"name": "Minsk", "lat": 53.9045, "lon": 27.5615},
    {"name": "Bucharest", "lat": 44.4268, "lon": 26.1025},
    {"name": "Sofia", "lat": 42.6977, "lon": 23.3219},
    {"name": "Belgrade", "lat": 44.7866, "lon": 20.4489},
    {"name": "Zagreb", "lat": 45.8150, "lon": 15.9819},
    {"name": "Budapest", "lat": 47.4979, "lon": 19.0402},
    {"name": "Prague", "lat": 50.0755, "lon": 14.4378},
    {"name": "Bratislava", "lat": 48.1486, "lon": 17.1077},
    {"name": "Riga", "lat": 56.9496, "lon": 24.1052},
    {"name": "Vilnius", "lat": 54.6872, "lon": 25.2797},
    {"name": "Tallinn", "lat": 59.4370, "lon": 24.7536},
    {"name": "Cairo", "lat": 30.0444, "lon": 31.2357},
    {"name": "Nairobi", "lat": -1.2921, "lon": 36.8219},
    {"name": "Lagos", "lat": 6.5244, "lon": 3.3792},
    {"name": "Casablanca", "lat": 33.5731, "lon": -7.5898},
    {"name": "Johannesburg", "lat": -26.2041, "lon": 28.0473},
    {"name": "Addis Ababa", "lat": 8.9806, "lon": 38.7578},
    {"name": "Accra", "lat": 5.6037, "lon": -0.1870},
    {"name": "Dakar", "lat": 14.7167, "lon": -17.4677},
    {"name": "Algiers", "lat": 36.7538, "lon": 3.0588},
    {"name": "Tunis", "lat": 36.8065, "lon": 10.1815},
    {"name": "Khartoum", "lat": 15.5007, "lon": 32.5599},
    {"name": "Dubai", "lat": 25.2048, "lon": 55.2708},
    {"name": "Riyadh", "lat": 24.7136, "lon": 46.6753},
    {"name": "Baghdad", "lat": 33.3152, "lon": 44.3661},
    {"name": "Tehran", "lat": 35.6892, "lon": 51.3890},
    {"name": "Karachi", "lat": 24.8607, "lon": 67.0011},
    {"name": "Mumbai", "lat": 19.0760, "lon": 72.8777},
    {"name": "New Delhi", "lat": 28.6139, "lon": 77.2090},
    {"name": "Kolkata", "lat": 22.5726, "lon": 88.3639},
    {"name": "Dhaka", "lat": 23.8103, "lon": 90.4125},
    {"name": "Yangon", "lat": 16.8661, "lon": 96.1951},
    {"name": "Bangkok", "lat": 13.7563, "lon": 100.5018},
    {"name": "Ho Chi Minh City", "lat": 10.8231, "lon": 106.6297},
    {"name": "Singapore", "lat": 1.3521, "lon": 103.8198},
    {"name": "Kuala Lumpur", "lat": 3.1390, "lon": 101.6869},
    {"name": "Jakarta", "lat": -6.2088, "lon": 106.8456},
    {"name": "Manila", "lat": 14.5995, "lon": 120.9842},
    {"name": "Hong Kong", "lat": 22.3193, "lon": 114.1694},
    {"name": "Taipei", "lat": 25.0330, "lon": 121.5654},
    {"name": "Seoul", "lat": 37.5665, "lon": 126.9780},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Beijing", "lat": 39.9042, "lon": 116.4074},
    {"name": "Shanghai", "lat": 31.2304, "lon": 121.4737},
    {"name": "Ulaanbaatar", "lat": 47.8864, "lon": 106.9057},
    {"name": "Almaty", "lat": 43.2220, "lon": 76.8512},
    {"name": "Tashkent", "lat": 41.2995, "lon": 69.2401},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
    {"name": "Melbourne", "lat": -37.8136, "lon": 144.9631},
    {"name": "Auckland", "lat": -36.8485, "lon": 174.7633},
    {"name": "Honolulu", "lat": 21.3069, "lon": -157.8583},
    {"name": "Anchorage", "lat": 61.2181, "lon": -149.9003},
    {"name": "Vancouver", "lat": 49.2827, "lon": -123.1207},
    {"name": "Seattle", "lat": 47.6062, "lon": -122.3321},
    {"name": "San Francisco", "lat": 37.7749, "lon": -122.4194},
    {"name": "Los Angeles", "lat": 34.0522, "lon": -118.2437},
    {"name": "Las Vegas", "lat": 36.1699, "lon": -115.1398},
    {"name": "Denver", "lat": 39.7392, "lon": -104.9903},
    {"name": "Chicago", "lat": 41.8781, "lon": -87.6298},
    {"name": "Miami", "lat": 25.7617, "lon": -80.1918},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Montreal", "lat": 45.5017, "lon": -73.5673},
    {"name": "Toronto", "lat": 43.6532, "lon": -79.3832},
    {"name": "Mexico City", "lat": 19.4326, "lon": -99.1332},
    {"name": "Havana", "lat": 23.1136, "lon": -82.3666},
    {"name": "Bogota", "lat": 4.7110, "lon": -74.0721},
    {"name": "Lima", "lat": -12.0464, "lon": -77.0428},
    {"name": "Santiago", "lat": -33.4489, "lon": -70.6693},
    {"name": "Buenos Aires", "lat": -34.6037, "lon": -58.3816},
    {"name": "Sao Paulo", "lat": -23.5505, "lon": -46.6333},
    {"name": "Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"name": "Caracas", "lat": 10.4806, "lon": -66.9036},
    {"name": "Quito", "lat": -0.1807, "lon": -78.4678},
    {"name": "Montevideo", "lat": -34.9011, "lon": -56.1645},
    {"name": "Kabul", "lat": 34.5553, "lon": 69.2075},
    {"name": "Islamabad", "lat": 33.7215, "lon": 73.0433},
    {"name": "Colombo", "lat": 6.9271, "lon": 79.8612},
    {"name": "Kathmandu", "lat": 27.7172, "lon": 85.3240},
    {"name": "Tbilisi", "lat": 41.6941, "lon": 44.8337},
    {"name": "Yerevan", "lat": 40.1872, "lon": 44.5152},
    {"name": "Baku", "lat": 40.4093, "lon": 49.8671},
    {"name": "Amman", "lat": 31.9454, "lon": 35.9284},
    {"name": "Tel Aviv", "lat": 32.0853, "lon": 34.7818},
    {"name": "Beirut", "lat": 33.8938, "lon": 35.5018},
    {"name": "Muscat", "lat": 23.5880, "lon": 58.3829},
    {"name": "Doha", "lat": 25.2854, "lon": 51.5310},
    {"name": "Kuwait City", "lat": 29.3759, "lon": 47.9774},
    {"name": "Ankara", "lat": 39.9334, "lon": 32.8597},
]


def fetch_temperatures(cities):
    lats = ",".join(str(c["lat"]) for c in cities)
    lons = ",".join(str(c["lon"]) for c in cities)
    resp = http.get(
        "https://api.open-meteo.com/v1/forecast",
        params={"latitude": lats, "longitude": lons, "current_weather": "true"},
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, dict):
        data = [data]
    results = []
    for i, item in enumerate(data):
        if i >= len(cities):
            break
        cw = item.get("current_weather", {})
        if "temperature" in cw:
            results.append({"name": cities[i]["name"], "temp": cw["temperature"]})
    return results


@app.route("/api/weather")
def weather():
    try:
        target = float(request.args.get("temp", 20))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid temperature parameter"}), 400

    all_results = []
    batch_size = 50
    for i in range(0, len(CITIES), batch_size):
        batch = CITIES[i : i + batch_size]
        try:
            all_results.extend(fetch_temperatures(batch))
        except Exception as e:
            return jsonify({"error": str(e)}), 502

    all_results.sort(key=lambda x: abs(x["temp"] - target))
    matches = [
        {**r, "diff": round(abs(r["temp"] - target), 1)}
        for r in all_results[:2]
    ]

    return jsonify({"target": target, "matches": matches})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
