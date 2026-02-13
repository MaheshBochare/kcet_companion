#!/usr/bin/env bash
set -o errexit

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec gunicorn kcet_backend.wsgi:application \
  --bind 0.0.0.0:${PORT} \
  --workers 2 \
  --threads 4
