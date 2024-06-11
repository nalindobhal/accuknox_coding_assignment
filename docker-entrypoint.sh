#!/bin/ash

echo "${0}: Running makemigrations"
python manage.py makemigrations
echo "${0}: Running migrate"
python manage.py migrate
echo "${0}: Creating Cache table"
python manage.py createcachetable

echo "${0}: Collecting static files."
python manage.py collectstatic --no-input --clear

#exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 config.wsgi:application

echo "${0}: All commands executed, exiting..."
exec "$@"