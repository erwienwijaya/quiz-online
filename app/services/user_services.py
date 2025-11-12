from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, username: str, password: str):
        username = (username or "").strip()
        if not username:
            raise ValueError("Nama pengguna wajib diisi.")
        if len(username) < 3:
            raise ValueError("Nama pengguna minimal 3 karakter.")

        if not password or len(password) < 6:
            raise ValueError("Password minimal 6 karakter.")

        existing = self.user_repo.get_by_username(username)
        if existing:
            raise ValueError("Nama pengguna sudah digunakan.")

        pwd_hash = generate_password_hash(password)
        user = self.user_repo.create(username=username, password_hash=pwd_hash)
        return user

    def update_profile(self, user_id: int, nim: str, firstname: str, lastname: str):
        nim = (nim or "").strip()
        firstname = (firstname or "").strip()
        lastname = (lastname or "").strip()

        if not nim:
            raise ValueError("NIM wajib diisi.")
        if not firstname:
            raise ValueError("Nama depan wajib diisi.")
        if not lastname:
            raise ValueError("Nama belakang wajib diisi.")

        user = self.user_repo.update_profile(
            user_id=user_id,
            nim=nim,
            firstname=firstname,
            lastname=lastname
        )
        if not user:
            raise ValueError("Pengguna tidak ditemukan.")
        return user

    def verify_password(self, password: str, password_hash: str) -> bool:
        return check_password_hash(password_hash, password)
