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

    # def __init__(self, db_session):
    #     self.db_session = db_session

    # def get_user(self, user_id):
    #     return self.db_session.query(User).filter(User.id == user_id).first()

    # def create_user(self, user_data):
    #     new_user = User(**user_data)
    #     self.db_session.add(new_user)
    #     self.db_session.commit()
    #     return new_user

    # def update_user(self, user_id, user_data):
    #     user = self.get_user(user_id)
    #     if user:
    #         for key, value in user_data.items():
    #             setattr(user, key, value)
    #         self.db_session.commit()
    #     return user

    # def delete_user(self, user_id):
    #     user = self.get_user(user_id)
    #     if user:
    #         self.db_session.delete(user)
    #         self.db_session.commit()
    #     return user
