from typing import Any

from flask_restful import Resource


class FindResource(Resource):
    def get(self) -> Any:
        return {'dummy': 'OK'}, 200

    def post(self) -> Any:
        return {'dummy': 'OK'}, 200
