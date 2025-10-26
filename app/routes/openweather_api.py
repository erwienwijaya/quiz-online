# routes/api.py
from flask import Blueprint, request, jsonify
from config import Config
from app.repositories.openweather_repository import OpenWeatherRepository
from app.services.openweather_services import OpenWeatherServices

weather_bp = Blueprint("api", __name__, url_prefix="/api")

_repo = OpenWeatherRepository(Config.OPENWEATHER_API_KEY)
_svc = OpenWeatherServices(_repo, country_code=Config.OPENWEATHER_COUNTRY_CODE)


class OpenWeatherAPI:
    @staticmethod
    def register_routes(weather_bp):
        @weather_bp.get("/forecast")
        def forecast():
            city = request.args.get("city", "").strip()
            if not city:
                return jsonify({"error": "Parameter 'city' wajib diisi."}), 400
            try:
                data = _svc.get_three_day_forecast(city)
                return jsonify(data), 200
            except ValueError as ve:
                return jsonify({"error": str(ve)}), 404
            except Exception as e:
                return jsonify({"error": f"Gagal mengambil data cuaca: {e}"}), 500


OpenWeatherAPI.register_routes(weather_bp)
