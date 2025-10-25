from datetime import datetime
from app.models import db


class Score(db.Model):
    __tablename__ = "scores"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        "users.id"), unique=True, nullable=False)

    quiz_1 = db.Column(db.Integer, default=0, nullable=False)
    quiz_2 = db.Column(db.Integer, default=0, nullable=False)
    quiz_3 = db.Column(db.Integer, default=0, nullable=False)
    quiz_4 = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow,
                           onupdate=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("score", uselist=False))

    @property
    def total(self) -> int:
        return (self.quiz_1 or 0) + (self.quiz_2 or 0) + (self.quiz_3 or 0) + (self.quiz_4 or 0)

    def to_dict(self, with_user=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "quiz_1": self.quiz_1,
            "quiz_2": self.quiz_2,
            "quiz_3": self.quiz_3,
            "quiz_4": self.quiz_4,
            "total": self.total,
            "created_at": self.created_at.isoformat() + "Z",
            "updated_at": self.updated_at.isoformat() + "Z",
        }
        if with_user and self.user:
            data["user"] = {"id": self.user.id, "username": self.user.username}
        return data
