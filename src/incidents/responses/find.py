from flask_restful.fields import List, Nested

from src.incidents.responses.incident import incident_response

# Схема получения списка инцидентов при поиске
find_response = {'incidents': List(Nested(incident_response))}
