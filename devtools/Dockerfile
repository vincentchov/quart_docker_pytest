FROM python:3.10 as development_build

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.1.13 \
    POETRY_NO_INTERACTION=1 \
    PYTHONPATH=${PYTHONPATH}:${PWD}

RUN ["mkdir", "-p", "/home"]
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

RUN useradd -rm \
        -d /home/docker_user \
        -s /bin/bash \
        -u 1000 docker_user

USER docker_user
RUN ["mkdir", "-p", "/home/docker_user/cardsystem"]
WORKDIR /home/docker_user

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN python3 -m pip install --user --upgrade nox \
    && python3 -m pip install nox-poetry

COPY --chown=docker_user:docker_user ../poetry.lock ../pyproject.toml ../.* /home/docker_user/cardsystem/
WORKDIR /home/docker_user/cardsystem
ENV PATH="/home/docker_user/.local/bin:$PATH"

RUN ["poetry", "config", "virtualenvs.in-project", "true"] \
    && ["poetry", "run", "pip", "install", "-U", "pip"] \
    && ["poetry", "install", "--no-interaction"]

COPY --chown=docker_user:docker_user ../.* /home/docker_user/cardsystem/
COPY --chown=docker_user:docker_user ../docs /home/docker_user/cardsystem/docs
COPY --chown=docker_user:docker_user ../src /home/docker_user/cardsystem/src
COPY --chown=docker_user:docker_user ../tests /home/docker_user/cardsystem/tests
COPY --chown=docker_user:docker_user ../typings /home/docker_user/cardsystem/typings
