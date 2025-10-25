from app.services.introduction_services import IntroductionService


class IntroductionRoutes:
    @staticmethod
    def register_routes(app):
        @app.route("/introduction")
        def introduction():
            return IntroductionService.get_introduction()

        @app.route("/about")
        def about():
            return IntroductionService.get_about()
