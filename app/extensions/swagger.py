from flasgger import Swagger
from app.docs.swagger_config import swagger_template, swagger_config

swagger = Swagger(template=swagger_template, config=swagger_config)


class SwaggerExtension:
    @staticmethod
    def init_app(app):
        swagger.init_app(app)
