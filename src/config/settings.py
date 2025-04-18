from typing import Annotated

from pydantic import (
    BeforeValidator,
    PostgresDsn,
)
from pydantic_settings import BaseSettings

from src.utils.parsers import parse_nullable_value


class Config(BaseSettings):
    # Общие переменные проекта
    DEBUG: bool
    SECRET_KEY: str

    # База данных
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_PORT: Annotated[int | None, BeforeValidator(parse_nullable_value)] = None

    @property
    def sqlalchemy_url(self) -> str:
        """Строим URL для синхронного подключения к БД"""
        dsn = PostgresDsn.build(
            scheme='postgresql+psycopg2',
            username=self.DB_USER,
            password=self.DB_PASS,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
        return str(dsn)


settings = Config()  # type: ignore
