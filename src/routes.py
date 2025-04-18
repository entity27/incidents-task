from flask import Flask


def register_blueprints(app: Flask) -> None:
    """
    Регистрируем все endpoint'ы в сервисе
    """
    from src.incidents.routers import blueprint as incidents_blueprint

    app.register_blueprint(incidents_blueprint)
