from flask import Blueprint
from app.services.auth_services import AuthService


pages_bp = Blueprint('auth_pages', __name__)


class AuthPages:

    @staticmethod
    def register_routes(pages_bp):
        @pages_bp.get("/login")
        def login_page():
            return AuthService.get_login_page()

        @pages_bp.get("/register")
        def register_page():
            return AuthService.get_register_page()

        @pages_bp.get("/profile")
        def profile_page():
            return AuthService.get_profile_page()
