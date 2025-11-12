from flask import render_template


class DashboardRepository:
    @staticmethod
    def get_dashboard_page() -> str:
        quizzes = [
            {"id": 1, "title": "UTS", "description": "Bab 1-7",
                "date": "2025-11-01", "time": "10:00", "duration": "90 menit", "status": "pending"},
            {"id": 2, "title": "UAS", "description": "Bab 8-16",
                "date": "2025-12-05", "time": "09:00", "duration": "90 menit", "status": "pending"},
        ]

        return render_template("dashboard_user.html", quizzes=quizzes)
