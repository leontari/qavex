FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install -U pip && pip install .

COPY app/ ./src/

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "market_data.main"]
