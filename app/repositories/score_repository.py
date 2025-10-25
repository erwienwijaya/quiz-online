from typing import Optional, List
from app.models import db
from app.models.score import Score
from app.models.user import User


class ScoreRepository:
    def get_by_user_id(self, user_id: int) -> Optional[Score]:
        return Score.query.filter_by(user_id=user_id).first()

    def create_or_update(self, user_id: int, **scores) -> Score:
        s = self.get_by_user_id(user_id)
        if not s:
            s = Score(user_id=user_id, **scores)
            db.session.add(s)
        else:
            for k, v in scores.items():
                setattr(s, k, v)
        db.session.commit()
        return s

    def patch(self, user_id: int, **scores) -> Score:
        s = self.get_by_user_id(user_id)
        if not s:
            s = Score(user_id=user_id)
            db.session.add(s)
        for k, v in scores.items():
            if v is not None:
                setattr(s, k, v)
        db.session.commit()
        return s

    def list_all(self) -> List[Score]:
        return Score.query.join(User, User.id == Score.user_id)\
            .order_by((Score.quiz_1 + Score.quiz_2 + Score.quiz_3 + Score.quiz_4).desc(), User.username.asc())\
            .all()

    def delete_for_user(self, user_id: int) -> bool:
        s = self.get_by_user_id(user_id)
        if not s:
            return False
        db.session.delete(s)
        db.session.commit()
        return True
