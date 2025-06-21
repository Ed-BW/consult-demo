#!/bin/sh

# Force Railway deployment update - v2
# Set default values for environment variables
export PORT=${PORT:-8080}
export GUNICORN_WORKERS=${GUNICORN_WORKERS:-1}
export GUNICORN_TIMEOUT=${GUNICORN_TIMEOUT:-120}

echo "=== Railway Deployment Debug Info ==="
echo "PORT environment variable: $PORT"
echo "RAILWAY_ENVIRONMENT: $RAILWAY_ENVIRONMENT"
echo "Starting Django application on port $PORT with $GUNICORN_WORKERS workers"
echo "Deployment version: v2 - test scripts removed"
echo "====================================="

# Run Django migrations and setup
venv/bin/django-admin migrate
venv/bin/django-admin collectstatic --noinput
venv/bin/django-admin compress --force --engine jinja2

# Generate demo data if database is empty
venv/bin/django-admin generate_dummy_data || echo "Demo data generation failed or already exists"

echo "Starting gunicorn server..."
echo "Binding to 0.0.0.0:$PORT"

# Start gunicorn with explicit configuration
exec venv/bin/gunicorn \
  --bind 0.0.0.0:$PORT \
  --workers $GUNICORN_WORKERS \
  --timeout $GUNICORN_TIMEOUT \
  --access-logfile - \
  --error-logfile - \
  --log-level debug \
  --capture-output \
  consultation_analyser.wsgi:application
