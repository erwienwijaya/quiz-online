from flask import render_template


class IntroductionRepository:

    @staticmethod
    def get_introduction() -> str:
        return render_template("intro.html")

    @staticmethod
    def get_about() -> str:
        return render_template("about.html")
