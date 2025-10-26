from flask import Blueprint, render_template

weather_pages_bp = Blueprint("weather_pages", __name__)


@weather_pages_bp.get("/")
def weather_page():
    return render_template("weather.html")
