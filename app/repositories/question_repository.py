from typing import Optional, List
from app.models.question import db, Question


class QuestionRepository:
    def create(self, **kwargs) -> Question:
        q = Question(**kwargs)
        db.session.add(q)
        db.session.commit()
        return q

    def get(self, qid: int) -> Optional[Question]:
        return Question.query.get(qid)

    def list(self, created_by: int | None = None) -> List[Question]:
        q = Question.query
        if created_by is not None:
            q = q.filter_by(created_by=created_by)
        return q.order_by(Question.id.desc()).all()

    def update(self, q: Question, **kwargs) -> Question:
        for k, v in kwargs.items():
            setattr(q, k, v)
        db.session.commit()
        return q

    def delete(self, q: Question) -> None:
        db.session.delete(q)
        db.session.commit()
