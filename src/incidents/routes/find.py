from flask import request
from flask_restful import Resource, abort, marshal_with

from src.incidents.repositories.incident import IncidentRepository
from src.incidents.responses.find import find_response
from src.incidents.schemas.find import find_get_parser
from src.incidents.services.find import FindService
from src.utils.responses import HttpResponse


class FindResource(Resource):
    def __init__(
        self, service: FindService = FindService(repo=IncidentRepository())
    ) -> None:
        """
        Ресурс поиска по инцидентам
        """
        self._service = service

    @marshal_with(find_response)  # type: ignore[misc]
    def get(self) -> HttpResponse:
        """
        Ожидаем query-параметр `h` (хеш), выполняет поиск по хешу

        Returns:
            Список найденных инцидентов
        """
        hashed: str = find_get_parser.parse_args()['h']
        data = self._service.by_hash(hashed)
        return {'incidents': data}, 200

    @marshal_with(find_response)  # type: ignore[misc]
    def post(self) -> HttpResponse:
        """
        Ожидаем JSON, выполняет поиск по атрибутам

        Notes:
            Ищет совпадения по полученным данным в БД среди заголовков и тел

        Returns:
            Список найденных инцидентов
        """
        if not request.is_json:
            abort(http_status_code=400, message='Данные должны быть в формате JSON')

        values = request.get_json()
        data = self._service.by_values(values)

        return {'incidents': data}, 200
