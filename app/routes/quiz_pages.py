from flask import Blueprint, render_template
# from app.repositories.score_repository import ScoreRepository

pages_quiz_bp = Blueprint("quiz_pages", __name__)


class QuizPages:
    @staticmethod
    def register_routes(pages_quiz_bp):

        @pages_quiz_bp.get("/quiz")
        def quiz_page():
            return render_template("quiz.html")
