import requests
from datetime import datetime, timedelta, timezone
from flask import Blueprint, request, jsonify, current_app

weather_bp = Blueprint("weather_api", __name__, url_prefix="/api/weather")

GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"
ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"  # One Call 3.0
# https://api.openweathermap.org/data/2.5/onecall


@weather_bp.get("")
def get_weather():
    """
    Query: /api/weather?city=Bandung
    Langkah:
      1) Geocode -> lat/lon (city,ID)
      2) One Call -> daily[0..2] (hari ini, besok, lusa), ambil temp.morn/day/eve
    """
    api_key = current_app.config.get("OPENWEATHER_API_KEY") or ""
    country = current_app.config.get("OPENWEATHER_COUNTRY_CODE", "ID")

    city = (request.args.get("city") or "").strip()
    if not city:
        return jsonify({"error": "Parameter 'city' wajib diisi."}), 400
    if not api_key:
        return jsonify({"error": "OPENWEATHER_API_KEY belum dikonfigurasi."}), 500

    # 1) Geocoding
    try:
        gparams = {"q": f"{city},{country}", "limit": 1, "appid": api_key}
        gres = requests.get(GEOCODE_URL, params=gparams, timeout=10)
        gres.raise_for_status()
        gdata = gres.json()
        if not gdata:
            return jsonify({"error": f"Kota '{city}' tidak ditemukan di {country}."}), 404
        lat = gdata[0]["lat"]
        lon = gdata[0]["lon"]
        resolved_name = gdata[0].get("name") or city.title()
    except requests.RequestException as e:
        return jsonify({"error": f"Gagal geocoding: {e}"}), 502

    # 2) One Call daily
    try:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",         # Celsius
            "exclude": "minutely,hourly,alerts,current"
        }
        wres = requests.get(ONECALL_URL, params=params, timeout=10)
        wres.raise_for_status()
        w = wres.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Gagal mengambil data cuaca: {e}"}), 502

    # Ambil 3 hari (0: hari ini, 1: besok, 2: lusa)
    daily = (w.get("daily") or [])[:3]
    tz_offset = w.get("timezone_offset", 0)  # detik
    tz = timezone(timedelta(seconds=tz_offset))

    result = []
    for d in daily:
        dt = datetime.fromtimestamp(d["dt"], tz)
        item = {
            "date_iso": dt.date().isoformat(),
            # nama hari (English). Bisa diubah ke locale ID manual jika perlu
            "day_name": dt.strftime("%A"),
            "temp": {
                "morning": round(d.get("temp", {}).get("morn", 0)),
                "day":     round(d.get("temp", {}).get("day", 0)),
                "evening": round(d.get("temp", {}).get("eve", 0)),
            },
            "summary": {
                "main": (d.get("weather") or [{}])[0].get("main", ""),
                "desc": (d.get("weather") or [{}])[0].get("description", "")
            }
        }
        result.append(item)

    payload = {
        "city": resolved_name,
        "country": country,
        "lat": lat,
        "lon": lon,
        "days": result
    }
    return jsonify(payload), 200
