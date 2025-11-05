from app.services.introduction_services import IntroductionService


class IntroductionRoutes:
    @staticmethod
    def register_routes(app):
        @app.route("/salam-perkenalan")
        def introduction():
            return IntroductionService.get_introduction()

        @app.route("/tentang-aku")
        def about():
            return IntroductionService.get_about()
