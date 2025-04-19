FROM python:3.11.12-alpine

WORKDIR /app

COPY [ \
    "./requirements/requirements.tests.txt", \
    "./alembic.ini", \
    "./pyproject.toml", \
    "./" \
]

RUN apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev python3-dev && \
    pip install --no-cache-dir -r requirements.tests.txt && \
    apk del .build-deps

EXPOSE 8000

ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["pytest"]
