FROM python:3.11-slim-buster

ENV LANG=C.UTF-8 \
  POETRY_VERSION=1.3.1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME="/opt/poetry" \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN pip install --upgrade pip
RUN apt-get -y update && \
    apt-get install -y --no-install-recommends gcc python3-dev wget && \
    rm -rf /var/lib/apt/lists/* && \
    pip install "poetry==$POETRY_VERSION" && poetry --version


WORKDIR /opt/bhub


ADD src/poetry.lock src/pyproject.toml /opt/bhub/
RUN poetry install --no-dev --no-interaction --no-ansi


RUN rm -rf "$POETRY_CACHE_DIR"


ADD src .


WORKDIR /opt/bhub


CMD ["python", "app.py"]
