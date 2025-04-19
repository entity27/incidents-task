from typing import Any

from src.incidents import actions
from src.incidents.models import Incident
from src.incidents.repositories.incident import IncidentRepository


class ProblemsService:
    def __init__(self, repo: IncidentRepository) -> None:
        """
        Сервис логики взаимодействия с инцидентами
        """
        self._repo = repo

    def create(self, headers: dict[str, Any], body: dict[str, Any]) -> Incident:
        """
        Хеширует и создаёт инцидент

        Args:
            headers: Заголовки запроса
            body: Тело запроса

        Returns:
            Инцидент
        """
        hashed = actions.calculate_hash(headers, body)
        incident = self._repo.create(headers, body, hashed)
        return incident
