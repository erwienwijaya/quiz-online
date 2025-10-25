from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.repositories.question_repository import QuestionRepository
from app.services.question_services import QuestionService
from app import csrf


question_bp = Blueprint("question_api", __name__, url_prefix="/api/questions")

service = QuestionService(QuestionRepository())


class QuestionAPI:
    @staticmethod
    def register_routes(question_bp):
        @csrf.exempt
        @question_bp.post("")
        @jwt_required()
        def create_question():
            data = request.get_json(silent=True) or {}
            user_id = get_user_id()
            try:
                q = service.create(data, created_by=user_id)
                return jsonify({"message": "Soal berhasil dibuat", "question": q.to_dict()}), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        @question_bp.get("")
        @jwt_required(optional=True)
        def list_questions():
            items = service.repo.list()
            return jsonify([q.to_dict() for q in items]), 200

        @question_bp.get("/<int:qid>")
        def get_question(qid: int):
            q = service.repo.get(qid)
            if not q:
                return jsonify({"error": "Soal tidak ditemukan"}), 404
            return jsonify(q.to_dict()), 200

        @question_bp.put("/<int:qid>")
        @jwt_required()
        def update_question(qid: int):
            data = request.get_json(silent=True) or {}
            user_id = get_user_id()
            try:
                q = service.update(qid, data, requester_id=user_id)
                return jsonify({"message": "Soal diperbarui", "question": q.to_dict()}), 200
            except LookupError as e:
                return jsonify({"error": str(e)}), 404
            except PermissionError as e:
                return jsonify({"error": str(e)}), 403
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        @question_bp.delete("/<int:qid>")
        @jwt_required()
        def delete_question(qid: int):
            q = service.repo.get(qid)
            if not q:
                return jsonify({"error": "Soal tidak ditemukan"}), 404
            service.repo.delete(q)
            return jsonify({"message": "Soal dihapus"}), 200

        def get_user_id(optional: bool = False) -> int | None:
            if optional:
                uid = get_jwt_identity()
                return int(uid) if uid is not None else None
            uid = get_jwt_identity()
            return int(uid)


QuestionAPI.register_routes(question_bp)
