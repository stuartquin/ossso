#!/bin/bash
rm -rf /app/ossso_app/static
mkdir -p /app/ossso_app/static

poetry run python /app/ossso_app/manage.py migrate --noinput
poetry run python /app/ossso_app/manage.py collectstatic --noinput

cp -r /app/ossso_web/build /storage
