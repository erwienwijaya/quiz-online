from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func
from app.models import db
from app.models.question import Question
from app.models.score import Score
from app.repositories.score_repository import ScoreRepository

quiz_bp = Blueprint("quiz_api", __name__, url_prefix="/api/quiz")
score_repo = ScoreRepository()

# Helper


def current_uid() -> int:
    return int(get_jwt_identity())


def _quiz_field(n: int) -> str:
    if n not in (1, 2, 3, 4):
        raise ValueError("Nomor kuis tidak valid.")
    return f"quiz_{n}"


class QuizAPI:
    @staticmethod
    def register_routes(bp: Blueprint):

        # Status kuis untuk user login: mana yang sudah ditempuh
        @bp.get("/status")
        @jwt_required(optional=True)
        def quiz_status():
            uid = get_jwt_identity()
            completed = {1: False, 2: False, 3: False, 4: False}
            if uid is not None:
                s = score_repo.get_by_user_id(int(uid))
                if s:
                    completed = {
                        1: s.quiz_1 is not None and s.quiz_1 > 0,
                        2: s.quiz_2 is not None and s.quiz_2 > 0,
                        3: s.quiz_3 is not None and s.quiz_3 > 0,
                        4: s.quiz_4 is not None and s.quiz_4 > 0,
                    }
            return jsonify({"completed": completed}), 200

        # Mulai kuis: ambil 10 soal acak (tanpa kunci)
        @bp.post("/<int:quiz_no>/start")
        @jwt_required()
        def quiz_start(quiz_no: int):
            field = _quiz_field(quiz_no)

            # Cek apakah sudah pernah mengerjakan
            uid = current_uid()
            s = score_repo.get_by_user_id(uid)
            if s and getattr(s, field) and getattr(s, field) > 0:
                return jsonify({"error": f"Kuis {quiz_no} sudah ditempuh."}), 400

            # Ambil 10 soal acak (atau sebanyak yang tersedia jika <10)
            total = db.session.query(func.count(Question.id)).scalar() or 0
            if total == 0:
                return jsonify({"error": "Belum ada bank soal."}), 400
            limit = min(10, total)
            qs = (
                db.session.query(Question)
                .order_by(func.random())
                .limit(limit)
                .all()
            )

            questions = [{
                "id": q.id,
                "text": q.text,
                "option_a": q.option_a,
                "option_b": q.option_b,
                "option_c": q.option_c,
                "option_d": q.option_d,
            } for q in qs]

            return jsonify({"quiz": quiz_no, "count": len(questions), "questions": questions}), 200

        # Submit jawaban → koreksi → simpan skor → 100 max
        @bp.post("/<int:quiz_no>/submit")
        @jwt_required()
        def quiz_submit(quiz_no: int):
            field = _quiz_field(quiz_no)
            uid = current_uid()

            data = request.get_json(silent=True) or {}
            answers = data.get("answers") or {}
            # answers diharapkan: { "<question_id>": "a|b|c|d" , ... }

            if not isinstance(answers, dict) or not answers:
                return jsonify({"error": "Payload jawaban tidak valid."}), 400

            # Koreksi
            qids = [int(qid) for qid in answers.keys() if str(qid).isdigit()]
            if not qids:
                return jsonify({"error": "Tidak ada jawaban terkirim."}), 400

            db_questions = (
                db.session.query(Question.id, Question.answer_key)
                .filter(Question.id.in_(qids))
                .all()
            )
            answer_map = {qid: ak for (qid, ak) in db_questions}

            correct = 0
            for qid, ans in answers.items():
                try:
                    qid_int = int(qid)
                except:
                    continue
                ak = answer_map.get(qid_int)
                if not ak:  # soal tidak ditemukan/valid
                    continue
                if (ans or "").strip().lower() == (ak or "").strip().lower():
                    correct += 1

            # Skor: 10 poin per jawaban benar (maks 100)
            score_value = int(correct * 10)

            # Simpan ke tabel scores (tidak overwrite jika sudah ada nilai >0)
            s = score_repo.get_by_user_id(uid)
            if not s:
                s = Score(user_id=uid)
                db.session.add(s)
            current = getattr(s, field) or 0
            if current and current > 0:
                return jsonify({"error": f"Kuis {quiz_no} sudah pernah diselesaikan."}), 400

            setattr(s, field, score_value)
            db.session.commit()

            return jsonify({
                "message": "Jawaban disimpan",
                "quiz": quiz_no,
                "correct": correct,
                "total_questions": len(qids),
                "score": score_value
            }), 200


QuizAPI.register_routes(quiz_bp)
