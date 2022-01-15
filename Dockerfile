FROM node:lts-alpine3.14 AS docs
WORKDIR /app/ossso_web

COPY ossso_web/ossso/package.json /app/ossso_web
COPY ossso_web/ossso/package-lock.json /app/ossso_web
RUN npm ci

COPY ossso_web/ossso/ /app/ossso_web
RUN npm run build
RUN ls ./build

FROM python:3 AS django
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

RUN mkdir -p /storage
RUN mkdir -p /app/ossso_web/build
COPY --from=docs /app/ossso_web/build /app/ossso_web/build
