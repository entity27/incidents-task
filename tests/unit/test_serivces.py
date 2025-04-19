from src.incidents.actions import calculate_hash
from src.incidents.repositories.incident import IncidentRepository
from src.incidents.services.find import FindService
from src.incidents.services.problems import ProblemsService


def test_problems_service():
    """
    Проверяем, что создание инцидента через сервис работает
    """
    headers = {'some_header': 'value'}
    body = {'key': 'value'}
    hashed = calculate_hash(headers, body)

    service = ProblemsService(IncidentRepository())
    incident = service.create(headers, body)

    assert incident.id is not None
    assert incident.headers == headers
    assert incident.body == body
    assert incident.hash == hashed


def test_find_by_hash():
    """
    Проверяем, что сервис поиска по хешу исправен
    """
    service = ProblemsService(IncidentRepository())
    data = [
        ({'h': '1'}, {'b': '2'}),
        ({'h': {'some': 'value'}}, {'b': '4', 'c': 5}),
        ({'h': {'some': 'value'}}, {'c': 5, 'b': '4'}),
    ]
    hashed = calculate_hash(*data[-1])

    for item in data:
        service.create(*item)

    results = FindService(IncidentRepository()).by_hash(hashed)
    assert len(results) == 2


def test_find_by_values():
    """
    Проверяем, что сервис поиск по значениям исправен
    """
    service = ProblemsService(IncidentRepository())
    data = [
        ({'some': {'unique': {'header': True}}}, {'some': {'unique': {'body': True}}}),
        ({'some': {'unique': {'header': True}}}, {'some': {'unique': {'body': False}}}),
        (
            {'some': {'unique': {'header': False}}},
            {'some': {'unique': {'body': False}}},
        ),
    ]
    for item in data:
        service.create(*item)

    find_service = FindService(IncidentRepository())

    results = find_service.by_values(data[-1][0])
    assert len(results) == 1

    results = find_service.by_values(data[0][0])
    assert len(results) == 2

    results = find_service.by_values(data[-1][-1])
    assert len(results) == 2

    results = find_service.by_values(data[0][1])
    assert len(results) == 1
