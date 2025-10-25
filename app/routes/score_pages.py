from flask import Blueprint, render_template
from app.repositories.score_repository import ScoreRepository

pages_score_bp = Blueprint("score_pages", __name__)


class ScorePages:
    @staticmethod
    def register_routes(pages_score_bp):

        @pages_score_bp.get("/leaderboard")
        def leaderboard_page():
            repo = ScoreRepository()
            items = repo.list_all()
            return render_template("board_score.html", items=items)
