FROM python:3.11-slim

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY ../api/pyproject.toml /app/pyproject.toml
COPY ../api/poetry.lock /app/poetry.lock
COPY ../api /app

WORKDIR /app/aboba

RUN poetry install --no-root

EXPOSE 8000

CMD ["gunicorn", "aboba.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
