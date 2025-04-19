from typing import Any

from src.incidents.models import Incident
from src.incidents.repositories.incident import IncidentRepository


class FindService:
    def __init__(self, repo: IncidentRepository) -> None:
        """
        Сервис логики поиска по инцидентам
        """
        self._repo = repo

    def by_hash(self, hashed: str) -> list[Incident]:
        """
        Выполняем поиск инцидентов по хешу

        Args:
            hashed: Хеш-строка

        Returns:
            Список инцидентов
        """
        incidents = self._repo.find_by_hash(hashed)
        return incidents

    def by_values(self, values: dict[str, Any]) -> list[Incident]:
        """
        Выполняем поиск инцидентов по ключам и значениям

        Args:
            values: Словарь ключей со значениями для поиска

        Returns:
            Список инцидентов
        """
        incidents = self._repo.find_by_values(values)
        return incidents
