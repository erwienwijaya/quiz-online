from app.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    def __init__(self, dashboard_repo: DashboardRepository):
        self.dashboard_repo = dashboard_repo

    @staticmethod
    def get_dashboard_page() -> str:
        return DashboardRepository.get_dashboard_page()
