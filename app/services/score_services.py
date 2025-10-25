from typing import Dict, Any
from app.repositories.score_repository import ScoreRepository
from app.repositories.user_repository import UserRepository


class ScoreService:
    def __init__(self, score_repo: ScoreRepository, user_repo: UserRepository):
        self.score_repo = score_repo
        self.user_repo = user_repo

    def _coerce_int(self, v):
        if v is None or v == "":
            return 0
        try:
            return int(v)
        except ValueError:
            raise ValueError("Nilai skor harus bilangan bulat.")

    def _validate_payload(self, data: Dict[str, Any]) -> Dict[str, int]:
        q1 = self._coerce_int(data.get("quiz_1"))
        q2 = self._coerce_int(data.get("quiz_2"))
        q3 = self._coerce_int(data.get("quiz_3"))
        q4 = self._coerce_int(data.get("quiz_4"))

        for v in (q1, q2, q3, q4):
            if v < 0:
                raise ValueError("Skor tidak boleh negatif.")
        return {"quiz_1": q1, "quiz_2": q2, "quiz_3": q3, "quiz_4": q4}

    def upsert(self, user_id: int, data: Dict[str, Any]):
        if not self.user_repo.get_by_id(user_id):
            raise LookupError("User tidak ditemukan.")
        payload = self._validate_payload(data)
        return self.score_repo.create_or_update(user_id, **payload)

    def patch(self, user_id: int, data: Dict[str, Any]):
        if not self.user_repo.get_by_id(user_id):
            raise LookupError("User tidak ditemukan.")
        allowed = {k: data.get(k)
                   for k in ("quiz_1", "quiz_2", "quiz_3", "quiz_4")}
        patched = {}
        for k, v in allowed.items():
            if v is not None:
                patched[k] = self._coerce_int(v)
        return self.score_repo.patch(user_id, **patched)

    def get_user_total(self, user_id: int) -> int:
        s = self.score_repo.get_by_user_id(user_id)
        return s.total if s else 0

    def leaderboard(self):
        return self.score_repo.list_all()
