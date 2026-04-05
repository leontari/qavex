########## BUILDER ##########
FROM python:3.11-slim AS builder

RUN pip install uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY packages ./packages
COPY services/backend-api ./services/template-service

# install prod deps
RUN uv sync --frozen --no-dev --package template-service

########## RUNTIME ##########
FROM python:3.11-slim

WORKDIR /app

# copy installed .venv
COPY --from=builder /app/.venv ./.venv

# copy service's code
COPY services/template-service ./services/template-service
COPY packages ./packages

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
