from collections.abc import Generator

import pytest
from flask import Flask
from flask_sqlalchemy.session import Session
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.config.flask import FlaskConfig
from src.config.settings import settings
from src.config.setup import create_app, db


@pytest.fixture(scope='session')
def engine() -> Generator[Engine, None, None]:
    """
    Подключаемся к БД
    """
    engine = create_engine(settings.sqlalchemy_url)
    yield engine
    engine.dispose()


@pytest.fixture(scope='session')
def tables(engine) -> Generator[None, None, None]:
    """
    Создаём и удаляем таблицы до и после тестов
    """
    db.metadata.create_all(bind=engine)
    yield
    db.metadata.drop_all(bind=engine)


@pytest.fixture(scope='function', autouse=True)
def session(engine, tables) -> Generator[Session, None, None]:  # noqa
    """
    Устанавливаем глобальную сессию для `db` Flask'а
    """
    connection = engine.connect()
    transaction = connection.begin()
    session_cls = scoped_session(sessionmaker(bind=connection))

    db.session = session_cls
    yield session_cls()

    session_cls.remove()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope='function')
def app() -> Flask:
    """
    Создаём тестовый app
    """
    config = FlaskConfig
    config.TESTING = True
    flask = create_app(config)
    db.init_app(flask)
    return flask


@pytest.fixture(scope='function')
def client(app):
    """
    Возвращаем тестовый клиент (для возможных интеграционных тестов)
    """
    return app.test_client()
