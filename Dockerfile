# Stage 1: Builder
FROM python:3.12-slim as builder

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

RUN pip install poetry==1.8.2

COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Stage 2: Runtime
FROM python:3.12-slim as runtime

RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

ENV PYTHONPATH=/app

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY booktrack_fastapi ./booktrack_fastapi
COPY migrations ./migrations
COPY scripts ./scripts
COPY alembic.ini .

RUN adduser --disabled-password --gecos '' booktrack
RUN chown -R booktrack:booktrack /app
USER booktrack

EXPOSE 8000

CMD ["sh", "-c", "uvicorn booktrack_fastapi.main:app --host 0.0.0.0 --port $PORT --workers 1"]