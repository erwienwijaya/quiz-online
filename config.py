import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

    SECRET_KEY = os.getenv("SECRET_KEY", "only-me-and-dev-should-know")

    # JWT via cookie HttpOnly
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "only-me-and-dev-should-know")
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    # True conditional production only  (HTTPS)
    JWT_COOKIE_SECURE = False
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_COOKIE_CSRF_PROTECT = True            # activate CSRF cookie JWT
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60

    # OPENWWEATHER_API_KEY = "f5692e9aef80ea0b2c5b366927d2f753"
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
    OPENWEATHER_COUNTRY_CODE = "ID"
    OPENWEATHER_GEO_URL = "https://api.openweathermap.org/geo/1.0/direct"
    OPENWEATHER_FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

    MORNING_HOURS = list(range(6, 12))   # 06:00 - 11:59
    DAY_HOURS = list(range(12, 18))  # 12:00 - 17:59
    NIGHT_HOURS = list(range(18, 24))  # 18:00 - 23:59
