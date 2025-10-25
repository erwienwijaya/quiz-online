from flask import Blueprint, request, jsonify
from app.services.user_services import UserService
from app.services.auth_services import AuthService
from app.repositories.user_repository import UserRepository
from app.repositories.auth_repository import AuthRepository
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt,
    get_jwt_identity, set_access_cookies, unset_jwt_cookies,
    create_refresh_token, set_refresh_cookies, get_csrf_token
)
from app import csrf


api_bp = Blueprint("auth_api", __name__, url_prefix="/api")
user_service = UserService(UserRepository())
auth_service = AuthService(AuthRepository(UserRepository()))


class AuthAPI:

    @staticmethod
    def register_routes(api_bp):
        @api_bp.post("/register")
        def api_register():
            data = request.get_json(silent=True)
            username = data.get("username")
            password = data.get("password")

            try:
                user = user_service.register(
                    username=username, password=password)
                return jsonify({"message": "Registrasi berhasil", "user": user.to_dict()}), 201
            except ValueError as e:
                return jsonify({"error": str(e)}), 400

        @api_bp.get("/users")
        def api_list_users():
            repo = UserRepository()
            users = [u.to_dict() for u in repo.list_all()]
            return jsonify(users), 200

        @csrf.exempt
        @api_bp.post("/login")
        def api_login():
            data = request.get_json(silent=True) or request.form or {}
            username = (data.get("username") or "").strip()
            password = data.get("password") or ""

            if not username or not password:
                return jsonify({"error": "Username & password wajib diisi."}), 400

            user = auth_service.authenticate(username, password)
            if not user:
                return jsonify({"error": "Username atau password salah."}), 401

            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"username": user.username}
            )

            refresh_token = create_refresh_token(
                identity=str(user.id),
                additional_claims={"username": user.username}
            )

            csrf_access_token = get_csrf_token(access_token)
            csrf_refresh_token = get_csrf_token(refresh_token)

            resp = jsonify({
                "message": "Login berhasil",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "csrf_access_token": csrf_access_token,
                "csrf_refresh_token": csrf_refresh_token
            })
            set_access_cookies(resp, access_token)
            set_refresh_cookies(resp, refresh_token)
            return resp, 200

        @api_bp.post("/token/refresh")
        @jwt_required(refresh=True)
        def refresh_access():
            user_id = get_jwt_identity()  # string
            claims = {"username": get_jwt().get("username")}
            new_access = create_access_token(
                identity=user_id, additional_claims=claims)

            resp = jsonify({
                "message": "Access token diperbarui",
                "access_token": new_access
            })
            set_access_cookies(resp, new_access)
            return resp, 200

        @api_bp.post("/logout")
        def api_logout():
            resp = jsonify({"message": "Logout berhasil"})
            unset_jwt_cookies(resp)
            return resp, 200

        @api_bp.get("/me")
        @jwt_required()
        def api_me():
            user_id = get_jwt_identity()
            claims = get_jwt()
            return jsonify({
                "id": int(user_id),
                "username": claims.get("username")
            }), 200


AuthAPI.register_routes(api_bp)
