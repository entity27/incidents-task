from flask import Blueprint
from flask_restful import Api

from src.incidents.routes.find import FindResource
from src.incidents.routes.problems import ProblemsResource

"""
Регистрируем все endpoint'ы для домена
"""

blueprint = Blueprint(name='incidents', import_name=__name__)
api = Api(blueprint)

api.add_resource(FindResource, '/find')
api.add_resource(ProblemsResource, '/problems')
