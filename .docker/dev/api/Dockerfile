FROM python:3.11-slim

RUN pip install poetry

RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

ENV POETRY_VIRTUALENVS_CREATE=false
ENV PYTHONPATH=/app

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock
COPY ./aboba /app

WORKDIR /app

RUN poetry install --no-root

RUN python -m manage collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "aboba.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
