from typing import Any

from flask_restful import Resource


class ProblemsResource(Resource):
    def post(self) -> Any:
        return {'dummy': 'OK'}, 201
