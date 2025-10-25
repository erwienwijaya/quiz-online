from flask import Flask
from datetime import datetime
from config import Config
from app.models import db
from flask_wtf.csrf import CSRFProtect
from flask_jwt_extended import JWTManager, verify_jwt_in_request, get_jwt_identity, get_jwt
from dotenv import load_dotenv
load_dotenv()


csrf = CSRFProtect()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key = "super-secret-key"
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    jwt.init_app(app)

    @app.context_processor
    def inject_current_year():
        ctx = {'current_year': datetime.utcnow().year, 'current_user': None}
        try:
            verify_jwt_in_request(optional=True)
            uid = get_jwt_identity()
            claims = get_jwt()
            if uid:
                ctx['current_user'] = {
                    'id': int(uid),
                    'username': claims.get('username')
                }
        except Exception:
            pass
        return ctx

    # load all routes
    from app.routes import register_routes
    register_routes(app)

    from app.routes.auth_api import api_bp
    csrf.exempt(api_bp)

    from app.routes.question_api import question_bp
    csrf.exempt(question_bp)

    from app.routes.score_api import score_bp
    csrf.exempt(score_bp)

    from app.routes.quiz_api import quiz_bp
    csrf.exempt(quiz_bp)

    from app.routes.weather_api import weather_bp
    csrf.exempt(weather_bp)

    with app.app_context():
        db.create_all()

    return app
