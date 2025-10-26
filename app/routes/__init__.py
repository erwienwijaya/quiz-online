from .introduction_routes import IntroductionRoutes
from .auth_pages import AuthPages
from .score_pages import ScorePages
from .quiz_pages import QuizPages
from .auth_api import api_bp
from .question_api import question_bp
from .score_api import score_bp
from .quiz_api import quiz_bp
from .openweather_api import weather_bp
from .weather_pages import weather_pages_bp


def register_routes(app):
    IntroductionRoutes.register_routes(app)
    AuthPages.register_routes(app)
    ScorePages.register_routes(app)
    QuizPages.register_routes(app)
    app.register_blueprint(api_bp)
    app.register_blueprint(question_bp)
    app.register_blueprint(score_bp)
    app.register_blueprint(quiz_bp)
    app.register_blueprint(weather_bp)
    app.register_blueprint(weather_pages_bp)
