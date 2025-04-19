from typing import Any

from sqlalchemy import and_, or_

from src.config.setup import db
from src.incidents.models.incident import Incident


class IncidentRepository:
    """
    Взаимодействия с таблицей инцидентов
    """

    @staticmethod
    def create(headers: dict[str, Any], body: dict[str, Any], hashed: str) -> Incident:
        """
        Создаёт запись инцидента

        Args:
            headers: Заголовки запроса для сохранения
            body: Тело запроса для сохранения
            hashed: Хеш заголовков и тела

        Returns:
            Инцидент
        """
        incident = Incident(headers=headers, body=body, hash=hashed)
        db.session.add(incident)
        db.session.commit()
        return incident

    @staticmethod
    def find_by_hash(hashed: str) -> list[Incident]:
        """
        Выполняет поиск по значению хеша

        Args:
            hashed: Хеш, по которому выполнится поиск

        Returns:
            Список инцидентов
        """
        results: list[Incident] = Incident.query.filter_by(hash=hashed).all()
        return results

    @staticmethod
    def find_by_values(values: dict[str, Any]) -> list[Incident]:
        """
        Выполняет поиск среди заголовков и тел по значениям ключей

        Args:
            values: Словарь значений

        Returns:
            Список инцидентов
        """
        clause = and_(
            *(
                or_(
                    Incident.headers.contains({key: value}),
                    Incident.body.contains({key: value}),
                )
                for key, value in values.items()
            )
        )
        query = Incident.query.filter(clause)
        results: list[Incident] = query.all()
        return results
