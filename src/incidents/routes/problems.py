from flask import request
from flask_restful import Resource, abort, marshal_with

from src.incidents.repositories.incident import IncidentRepository
from src.incidents.responses.problems import problems_response
from src.incidents.services.problems import ProblemsService
from src.utils.responses import HttpResponse


class ProblemsResource(Resource):
    def __init__(
        self, service: ProblemsService = ProblemsService(repo=IncidentRepository())
    ) -> None:
        """
        Ресурс создания инцидентов
        """
        self._service = service

    @marshal_with(problems_response)  # type: ignore[misc]
    def post(self) -> HttpResponse:
        """
        Принимаем JSON запрос, создаём инцидент с телом и заголовками запроса

        Returns:
            Хеш инцидента
        """
        if not request.is_json:
            abort(http_status_code=400, message='Данные должны быть в формате JSON')

        headers = dict(request.headers.items())
        body = request.get_json()
        data = self._service.create(headers, body)

        return data, 201
