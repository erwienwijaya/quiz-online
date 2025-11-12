from app.repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self, auth_repo: AuthRepository):
        self.auth_repo = auth_repo

    def authenticate(self, username: str, password: str):
        """Gunakan AuthRepository untuk autentikasi user."""
        return self.auth_repo.authenticate(username, password)

    @staticmethod
    def get_login_page() -> str:
        return AuthRepository.get_login_page()

    @staticmethod
    def get_register_page() -> str:
        return AuthRepository.get_register_page()

    @staticmethod
    def get_profile_page() -> str:
        return AuthRepository.get_profile_page()
