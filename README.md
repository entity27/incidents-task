# incidents-task
Система сбора инцидентов. Тестовое задание в компанию «B».

# Структура проекта
- `alembic` - менеджмент миграций
- `docker` - файлы для апи, селери и проведения тестов
  - `scripts` - скрипты для использования внутри контейнеров
- `envs` - файлы с переменными окружения
  - `docker.incidents.env.example` - пример для докера
  - `local.incidents.env.example` - пример для локальной разработки
  - `postgres.env.example` - пример для postgresql контейнера
- `requirements` - зависимости
  - `requirements.txt` - для обычного контейнера
  - `requirements.test.txt` - для контейнера тестов
- `scripts` - утилиты для разработки
- `src` - исходный код проекта
  - `config` - общая кофигурация проекта
  - `utils` - полезные зависимости
  - `...` - доменные пакеты с моделями, роутами и т.п.
- `tests` - тесты

# Подготовка переменных окружения
В случае **локального** запуска
- Копируем `envs/local.incidents.env.example` -> `envs/local.incidents.env`

В случае запуска в **докере**
- Копируем `envs/docker.incidents.env.example` -> `envs/docker.incidents.env`

Настройка **PostgreSQL** контейнера
- Копируем `envs/postgres.env.example` -> `envs/postgres.env`

# Запуск проекта
## Локально

Через Poetry:
```bash
poetry install
```

Загрузка переменных окружения (при запуске в консоли)
```bash
. ./scripts/export_env.sh
```

Запуск API:
```bash
flask --app src.main run --port=8000
```

Хук для разработки:
```bash
pre-commit install
```

## Докер
```bash
docker compose up -d
```

# Обзор

## Стек
- `PostgreSQL` - база данных
- `Alembic` - миграции
- `SQLAlchemy` - ORM, через `flask-sqlalchemy`
- `Pytest` - тесты
- `Flask` + `Flask-Restful` - веб фреймворк
- `Docker` + `Docker Compose` - оркестрация
контейнеров зависимостей и проведение тестов

## API
### `POST /problems` - Записать инцидент
Записывает инцидент в БД, возвращает хеш

Принимает JSON
```json
{
  "some": {
    "unique": {
      "field": 1337
    }
  }
}
```

Сохраняет заголовки запроса, тело запроса, вычисляет для них хеш
(не зависит от порядка ключей на одном уровне)

Возвращает хеш:
```json
{
    "hash": "6b2cfa5431fdd509ff31847097995db384c72f62afa4ac1c8592f510a9e088f7"
}
```

### `POST /find` - Поиск инцидентов (по телу)
Выполняет поиск инцидентов по JSON телу запроса

Принимает JSON:
```json
{
    "some": {"unique": {"field": 1337}},
    "Host": "127.0.0.1:8000"
}
```

Выполняет поиск по каждой записи верхнего уровня.

К примеру, ищет `"some": ...` в заголовках и теле инцидентов,
а затем ищет `"Host": ...` в заголовках и теле инцидентов.

Возвращает такие значение, где все ключи есть хотя бы в одном месте,
т.е. либо в заголовках, либо в теле

Возвращает список подходящих инцидентов:
```json
{
    "incidents": [
        {
            "id": 13,
            "hash": "63bd7bae826f1198cd7710c7441a0c844b1f23ebad4a0dd8df28dfd968a56ddd",
            "body": {
                "some": {
                    "unique": {
                        "field": 1337
                    }
                }
            },
            "headers": {
                "Host": "127.0.0.1:8000",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "User-Agent": "PostmanRuntime/7.43.3",
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
                "Postman-Token": "6275425b-2b61-46c8-99ea-eac7dd0069fc",
                "Content-Length": "37",
                "Accept-Encoding": "gzip, deflate, br"
            }
        }
    ]
}
```

### `GET /find` - Поиск инцидентов (по хешу)
Выполняет поиск инцидентов по хешу, вернёт список
инцидентов с указанным хешем.

#### Query-параметры
- `h` - **обязателен**, принимает хеш искомого инцидента

Возвращает список инцидентов:
```json
{
    "incidents": [
        {
            "id": 2,
            "hash": "2b98383bf8c4d0e37c980b8b59d0c242f34f7b9e5a62ec09e4d341e6fe1dbc1c",
            "body": {
                "hello": 1248
            },
            "headers": {
                "Host": "127.0.0.1:8000",
                "Accept": "*/*",
                "Connection": "keep-alive",
                "User-Agent": "PostmanRuntime/7.43.3",
                "Content-Type": "application/json",
                "Cache-Control": "no-cache",
                "Postman-Token": "f45f9523-ecb7-41d5-b505-176d7483c7cd",
                "Content-Length": "16",
                "Accept-Encoding": "gzip, deflate, br"
            }
        }
    ]
}
```
