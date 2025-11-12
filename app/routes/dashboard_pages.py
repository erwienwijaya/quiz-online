from flask import Blueprint
from app.services.dashboard_services import DashboardService

dashboard_bp = Blueprint('dashboard_pages', __name__)


class DashboardPages:
    @staticmethod
    def register_routes(dashboard_bp):

        @dashboard_bp.get("/dashboard")
        def dashboard_page():
            return DashboardService.get_dashboard_page()


DashboardPages.register_routes(dashboard_bp)
