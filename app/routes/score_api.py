from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.repositories.score_repository import ScoreRepository
from app.repositories.user_repository import UserRepository
from app.services.score_services import ScoreService

score_bp = Blueprint("score_api", __name__, url_prefix="/api/scores")
service = ScoreService(ScoreRepository(), UserRepository())


def current_uid_strict() -> int:
    return int(get_jwt_identity())


class ScoreAPI:
    @staticmethod
    def register_routes(bp: Blueprint):
        # Leaderboard (GET) - publik
        @bp.get("")
        def list_scores():
            items = service.leaderboard()
            return jsonify([s.to_dict(with_user=True) for s in items]), 200

        # Detail user (GET) - publik
        @bp.get("/<int:user_id>")
        def get_user_score(user_id: int):
            s = service.score_repo.get_by_user_id(user_id)
            if not s:
                return jsonify({"user_id": user_id, "quiz_1": 0, "quiz_2": 0, "quiz_3": 0, "quiz_4": 0, "total": 0}), 200
            return jsonify(s.to_dict(with_user=True)), 200

        # Total user (GET) - publik
        @bp.get("/<int:user_id>/total")
        def get_user_total(user_id: int):
            return jsonify({"user_id": user_id, "total": service.get_user_total(user_id)}), 200

        # Upsert penuh (POST/PUT) - butuh login (misal peran guru/admin)
        @bp.post("/<int:user_id>")
        @bp.put("/<int:user_id>")
        @jwt_required()
        def upsert_user_score(user_id: int):
            data = request.get_json(silent=True) or {}
            try:
                s = service.upsert(user_id, data)
                return jsonify({"message": "Skor disimpan", "score": s.to_dict()}), 200
            except LookupError as e:
                return jsonify({"error": str(e)}), 404
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        # Patch sebagian (PATCH) - butuh login
        @bp.patch("/<int:user_id>")
        @jwt_required()
        def patch_user_score(user_id: int):
            data = request.get_json(silent=True) or {}
            try:
                s = service.patch(user_id, data)
                return jsonify({"message": "Skor diperbarui", "score": s.to_dict()}), 200
            except LookupError as e:
                return jsonify({"error": str(e)}), 404
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        # Delete skor (opsional)
        @bp.delete("/<int:user_id>")
        @jwt_required()
        def delete_user_score(user_id: int):
            ok = service.score_repo.delete_for_user(user_id)
            if not ok:
                return jsonify({"error": "Skor tidak ditemukan"}), 404
            return jsonify({"message": "Skor dihapus"}), 200


ScoreAPI.register_routes(score_bp)
