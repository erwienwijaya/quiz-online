from typing import Optional, List
from app.models.user import db, User


class UserRepository:
    def create(self, username: str, password_hash: str) -> User:
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)
        db.session.commit()
        return user

    def get_by_username(self, username: str) -> Optional[User]:
        return User.query.filter_by(username=username).one_or_none()

    def list_all(self) -> List[User]:
        return User.query.order_by(User.id.asc()).all()

    def get_by_id(self, user_id: int):
        from app.models.user import User
        return User.query.get(user_id)
