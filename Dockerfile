# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Чтобы логи сразу печатались в консоль, без буферизации
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

ENV POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry-cache

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    zlib1g-dev \
    libjpeg62-turbo-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry 2.x
ARG POETRY_VERSION=2.0.1
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

# Копирование файлов зависимостей, чтобы лучше работал кеш Docker
COPY pyproject.toml poetry.lock* /app/

# Установка зависимости
RUN poetry install --no-root && rm -rf "$POETRY_CACHE_DIR"

# Копирование кода проекта
COPY . /app/

# Создание папки под статику/медиа
RUN mkdir -p /app/staticfiles /app/media

EXPOSE 8000

# Команда по умолчанию (dev-режим)
CMD ["bash", "-lc", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]