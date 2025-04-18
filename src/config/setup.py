from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from src.config.flask import FlaskConfig

# Объект для взаимодействия с БД
db = SQLAlchemy()


def create_app(config: type[FlaskConfig] = FlaskConfig) -> Flask:
    """
    Создаёт объект Flask приложения

    Args:
        config: Класс настроек
    """
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)

    return app
