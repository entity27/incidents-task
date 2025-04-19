from typing import Any

from sqlalchemy import Index, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from src.config.setup import db


class Incident(db.Model):  # type: ignore[name-defined]
    """
    Модель инцидентов

    Attributes:
        headers: JSONB набор значений заголовка запроса инцидента
        body: JSONB набор значений тела запроса инцидента
        hash: SHA256 хеш значений headers и body, порядок ключей на хеш не влияет

    Notes:
        Для JSONB колонок использует GIN индексы.
        GIN - Generalized Inverted Index.
        Хороши для поиска по составным значениям, таких как JSONB.

        Для хеша - обыкновенный индекс.

        Обилие индексов повлияет на скорость записи, но это trade-off между скоростью поиска.
        Селективность для hash'а должна быть высокой, поскольку в подобной таблице hash, как правило,
        будет достаточно уникальным (если планируем получать каждый раз разный payload)

        Если требуют, чтобы поиск работал максимально быстро, придётся использовать индексы
    """

    __tablename__ = 'incidents'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    hash: Mapped[str] = mapped_column(String(64), nullable=False, index=True)
    headers: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)
    body: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False)

    __table_args__ = (
        Index('ix_incidents_headers_gin', headers, postgresql_using='gin'),
        Index('ix_incidents_body_gin', body, postgresql_using='gin'),
    )
