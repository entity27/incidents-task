from flask_restful import reqparse

find_get_parser = reqparse.RequestParser()
find_get_parser.add_argument(
    'h',
    type=str,
    required=True,
    help='Необходимо указать хеш инцидента для выполнения поиска',
    location='args',
)
