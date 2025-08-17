# syntax=docker/dockerfile:1
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Встановлення залежностей, якщо є requirements.txt
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

# Копіюємо весь код застосунку
COPY .. /app

# Порт, який слухає застосунок (оновіть у коді на 0.0.0.0, якщо потрібно)
EXPOSE 3000

# Точка входу
CMD ["python", "server.py"]
