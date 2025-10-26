from flask import render_template
from werkzeug.security import check_password_hash
from app.repositories.user_repository import UserRepository


class AuthRepository:
    def __init__(self, user_repo: UserRepository = None):
        self.user_repo = user_repo or UserRepository()

    @staticmethod
    def get_login_page() -> str:
        return render_template("auth/login.html")

    @staticmethod
    def get_register_page() -> str:
        return render_template("auth/register.html")

    def authenticate(self, username: str, password: str):
        user = self.user_repo.get_by_username((username).strip())
        if not user:
            return None
        if not check_password_hash(user.password_hash, password or ""):
            return None
        return user
