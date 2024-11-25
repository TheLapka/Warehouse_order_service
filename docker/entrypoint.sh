#!/bin/sh

# echo Starting collecting static

# python manage.py collectstatic --noinput || exit 1

echo Starting migrations

python manage.py migrate --noinput || exit 1

echo Migrations is done!

python manage.py runserver 0.0.0.0:8000
