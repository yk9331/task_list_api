FROM python:3.10-slim as builder

RUN pip install poetry==1.8.2

WORKDIR /app

COPY pyproject.toml poetry.lock /app

ENV POETRY_NO_INTERACTION=1
ENV POETRY_VIRTUALENVS_IN_PROJECT=1 
ENV POETRY_VIRTUALENVS_CREATE=1 
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install --only main --no-root

FROM python:3.10-slim as base

COPY --from=builder /app/.venv /app/.venv
COPY . /app/code

WORKDIR /app/code

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"] 