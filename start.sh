#!/bin/sh

# Set default values for environment variables
export PORT=${PORT:-8000}
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-2}
export GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}

echo "Starting application on port $PORT with $GUNICORN_WORKERS workers"

venv/bin/django-admin migrate
venv/bin/django-admin collectstatic --noinput
venv/bin/django-admin compress --force --engine jinja2

# Generate demo data if database is empty
venv/bin/django-admin generate_dummy_data || echo "Demo data generation failed or already exists"

# Start gunicorn with explicit configuration
exec venv/bin/gunicorn \
  --bind 0.0.0.0:$PORT \
  --workers $GUNICORN_WORKERS \
  --timeout $GUNICORN_TIMEOUT \
  --access-logfile - \
  --error-logfile - \
  --log-level info \
  consultation_analyser.wsgi:application
