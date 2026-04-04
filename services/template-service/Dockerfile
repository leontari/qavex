# services/backend-api/Dockerfile.prod

########## BUILDER ##########
FROM python:3.11-slim AS builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages ./packages
COPY services/backend-api ./services/backend-api

# Устанавливаем только продакшен зависимости
RUN uv sync --frozen --no-dev --package backend-api

########## RUNTIME ##########
FROM python:3.11-slim

WORKDIR /app

# Копируем установленное окружение
COPY --from=builder /app/.venv ./.venv

# Копируем код сервиса
COPY services/backend-api ./services/backend-api
COPY packages ./packages

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
