from app.repositories.introduction_repository import IntroductionRepository


class IntroductionService:
    @staticmethod
    def get_introduction() -> str:
        return IntroductionRepository.get_introduction()

    @staticmethod
    def get_about() -> str:
        return IntroductionRepository.get_about()
