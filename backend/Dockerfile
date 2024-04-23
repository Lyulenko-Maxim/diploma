FROM python:3.11-alpine3.19 as base

ARG DEBUG=0
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

RUN apk update && \
    apk add libpq


FROM base as builder

ENV POETRY_VERSION=1.6.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apk update && \
    apk add musl-dev build-base gcc gfortran openblas-dev postgresql-client postgresql-dev

WORKDIR /app

RUN pip install poetry==$POETRY_VERSION
COPY pyproject.toml poetry.lock ./

RUN if [ $DEBUG ]; then \
      poetry install --with dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    else \
      poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR; \
    fi


FROM base as runtime

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY . /app

WORKDIR /app

EXPOSE 8000