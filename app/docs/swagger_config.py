"""
Swagger configuration module
----------------------------
This module centralizes all Swagger (Flasgger) settings and documentation metadata
for the Flask application.

Best practice: Keep your Swagger template & config separate from
the main app factory to improve readability and maintainability.
"""

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Quiz Online API",
        "description": (
            "This API provides endpoints for user authentication and quiz management. "
            "It follows RESTful principles and uses JWT for secure authentication.\n\n"
            "### 🔐 Authentication Notes\n"
            "- After login, `access_token` and `refresh_token` are stored in cookies.\n"
            "- CSRF tokens are included in the response body for both tokens.\n"
            "- To access protected endpoints, send the `X-CSRF-TOKEN` header "
            "with the `csrf_access_token` value.\n\n"
            "### 📘 Swagger Usage\n"
            "Use the 'Try it out' feature to test endpoints directly from the UI."
        ),
        "version": "1.0.0",
        "contact": {
            "name": "API Support",
            "url": "https://github.com/erwienwijaya",
            "email": "erwin.cipta@gmail.com",
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT",
        },
    },
    "basePath": "/api",  # all APIs under /api
    "schemes": ["http"],
    "tags": [
        {
            "name": "Auth",
            "description": "Endpoints related to user authentication (login, refresh, logout)",
        },
        {
            "name": "User",
            "description": "Endpoints for managing user profiles and accounts",
        },
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'",
        }
    },
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "swagger_spec",
            "route": "/swagger.json",
            "rule_filter": lambda rule: True,  # include all routes
            "model_filter": lambda tag: True,  # include all models
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/docs/",  # Swagger UI available at /docs/
    "title": "Quiz Online API Docs",
    "uiversion": 3,
}
