from src.config.settings import settings


class FlaskConfig:
    """
    Класс конфигурации для Flask'а
    """

    SQLALCHEMY_DATABASE_URI = settings.sqlalchemy_url
    SECRET_KEY = settings.SECRET_KEY
    DEBUG = settings.DEBUG
