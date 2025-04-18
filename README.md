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

### `POST /find` - Поиск инцидентов (по телу)
Выполняет поиск инцидентов по JSON телу запроса

### `GET /find` - Поиск инцидентов (по хешу)
Выполняет поиск инцидентов по хешу, вернёт список
инцидентов с указанным хешем.

#### Query-параметры
- `h` - **обязателен**, принимает хеш искомого инцидента
