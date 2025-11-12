from datetime import datetime
from app.models import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True,
                         nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    nim = db.Column(db.String(20), nullable=True)
    firstname = db.Column(db.String(80), nullable=True)
    lastname = db.Column(db.String(120), nullable=True)
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nim": self.nim,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "created_at": self.created_at.isoformat() + "Z",
        }
