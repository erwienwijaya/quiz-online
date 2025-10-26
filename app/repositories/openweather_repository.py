# repositories/openweather_repository.py
import requests
from config import Config


class OpenWeatherRepository:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.geo_url = Config.OPENWEATHER_GEO_URL
        self.forecast_url = Config.OPENWEATHER_FORECAST_URL

    def _assert_api_key(self):
        if not self.api_key:
            raise RuntimeError(
                "OPENWEATHER_API_KEY tidak ditemukan. periksa pengaturan environment.")

    def geocode_city(self, city_name: str, country_code: str):
        """Return {'name','lat','lon'} for city + country code."""
        self._assert_api_key()
        params = {"q": f"{city_name},{country_code}",
                  "limit": 1, "appid": self.api_key}
        r = requests.get(self.geo_url, params=params, timeout=15)
        r.raise_for_status()
        data = r.json()
        if not data:
            raise ValueError(
                f"Kota '{city_name}' tidak ditemukan di {country_code}.")
        item = data[0]
        return {"name": item.get("name"), "lat": item["lat"], "lon": item["lon"]}

    def get_5day_3hour_forecast(self, lat: float, lon: float, units: str = "metric", lang: str = "id"):
        """Return raw JSON from 5-day/3-hour forecast endpoint."""
        self._assert_api_key()
        params = {"lat": lat, "lon": lon,
                  "appid": self.api_key, "units": units, "lang": lang}
        r = requests.get(self.forecast_url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
