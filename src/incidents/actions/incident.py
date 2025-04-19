import json
from hashlib import sha256
from typing import Any


def calculate_hash(headers: dict[str, Any], body: dict[str, Any]) -> str:
    """
    Выполняет расчёт SHA-256 хеша по словарям заголовков запроса и тела запроса

    Args:
        headers: Заголовки запроса
        body: Тело запроса

    Notes:
        Словари преобразуются в JSON строку с сортировкой по ключам.

        Сортировка необходима для получения одинакового набора значений хеша
        при различном порядке ключей в словарях

    Returns:
        SHA-256 хеш
    """
    data = json.dumps(obj={'1': headers, '2': body}, sort_keys=True)
    hashed = sha256(data.encode(encoding='UTF-8'))
    return hashed.hexdigest()
