from flask_restful.fields import Integer, Raw, String

# Схема получения инцидента
incident_response = {
    'id': Integer,
    'hash': String,
    'body': Raw,
    'headers': Raw,
}
