FROM python:3
ENV PYTHONUNBUFFERED=1

RUN apt update && \
    apt install -y xmlsec1
RUN pip install poetry

COPY ossso_app /app/ossso_app

WORKDIR /app/ossso_app
RUN poetry install
