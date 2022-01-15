FROM python:3
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y xmlsec1
RUN pip install poetry

WORKDIR /app
ADD ossso_app/poetry.lock /app/poetry.lock
ADD ossso_app/pyproject.toml /app/pyproject.toml
RUN poetry install --no-dev

ADD Procfile /app/Procfile
ADD dokku/nginx.conf.sigil /app/nginx.conf.sigil
ADD dokku/release-tasks.sh /app/release-tasks.sh

COPY ossso_app /app/ossso_app
