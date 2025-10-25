from typing import Dict, Any
from app.repositories.question_repository import QuestionRepository

ALLOWED_KEYS = {"a", "b", "c", "d"}


class QuestionService:
    def __init__(self, repo: QuestionRepository):
        self.repo = repo

    def _validate_payload(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Normalisasi input
        text = (data.get("text") or "").strip()

        option_a = (data.get("option_a") or "").strip()
        option_b = (data.get("option_b") or "").strip()
        option_c = (data.get("option_c") or "").strip()
        option_d = (data.get("option_d") or "").strip()

        answer_key = (data.get("answer_key") or "").strip().lower()

        # Validation
        if not text:
            raise ValueError("Teks soal wajib diisi.")
        if not option_a or not option_b or not option_c or not option_d:
            raise ValueError("Semua opsi (a,b,c,d) wajib diisi.")
        if answer_key not in ALLOWED_KEYS:
            raise ValueError(
                "Kunci jawaban harus salah satu dari: a, b, c, d.")

        if answer_key == "a" and not option_a:
            raise ValueError("Opsi A kosong.")
        if answer_key == "b" and not option_b:
            raise ValueError("Opsi B kosong.")
        if answer_key == "c" and not option_c:
            raise ValueError("Opsi C kosong.")
        if answer_key == "d" and not option_d:
            raise ValueError("Opsi D kosong.")

        return {
            "text": text,
            "option_a": option_a,
            "option_b": option_b,
            "option_c": option_c,
            "option_d": option_d,
            "answer_key": answer_key,
        }

    def create(self, data: Dict[str, Any], created_by: int | None = None):
        payload = self._validate_payload(data)
        if created_by:
            payload["created_by"] = created_by
        return self.repo.create(**payload)

    def update(self, qid: int, data: Dict[str, Any], requester_id: int | None = None):
        q = self.repo.get(qid)
        if not q:
            raise LookupError("Soal tidak ditemukan.")
        payload = self._validate_payload({**q.to_dict(), **data})
        # (opsional) hak edit hanya creator
        # if requester_id and q.created_by and q.created_by != requester_id:
        #     raise PermissionError("Anda tidak berhak mengubah soal ini.")
        return self.repo.update(q, **payload)
