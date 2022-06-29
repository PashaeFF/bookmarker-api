template = {
    "swagger": "2.0",
    "info": {
        "title": "Bookmarks API",
        "description": "API for bookmarks",
        "contact": {
            "responsibleOrganization": "",
            "responsibleDeveloper": "",
            "email": "dev@gmail.com",
            "url": "www.fb.com/dev",
        },
        "termsOfService": "www.fb.com/dev",
        "version": "1.0"
    },
    "basePath": "/api/v1",
    "schemes": [
        "http",
        "https"
    ],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: \"Authorization: Bearer {token}\""
            }
        },
    }

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True, #all in
            "model_filter": lambda tag: True, #all in
            }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
} 