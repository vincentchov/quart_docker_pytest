FROM python:3.10 as development_build

ARG QUART_ENV

ENV QUART_ENV=${QUART_ENV} \
    QUART_APP=quart_docker_pytest.api:create_app() \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local' \
    PYTHONPATH=${PYTHONPATH}:${PWD}

RUN mkdir /app
RUN mkdir /app/src

WORKDIR /app

RUN groupadd -r web \
    && useradd -d /app -r -g web web \
    && chown web:web -R /app

RUN curl -sSL https://install.python-poetry.org | python3 -

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

RUN poetry install --no-dev

RUN echo "$QUART_ENV" \
    && poetry version \
    && poetry run pip install -U pip \
    && poetry install \
        $(if [ "$QUART_ENV" = 'production' ]; then echo '--no-dev'; fi) \
        --no-interaction --no-ansi \
    && if [ "$QUART_ENV" = 'production' ]; then rm -rf "$POETRY_CACHE_DIR"; fi

USER web

WORKDIR /app/src

FROM development_build AS production_build

COPY --chown=web:web /src/quart_docker_pytest /app/src/quart_docker_pytest
CMD ["hypercorn", "quart_docker_pytest.api:create_app()", "-w", "2", "-b", "0.0.0.0:80"]

FROM development_build AS management_build
ENTRYPOINT ["poetry", "run", "quart-docker-pytest"]
