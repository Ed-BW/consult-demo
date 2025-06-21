#!/bin/sh

venv/bin/django-admin migrate
venv/bin/django-admin collectstatic --noinput
venv/bin/django-admin compress --force --engine jinja2

# Generate demo data if database is empty
venv/bin/django-admin generate_dummy_data --respondents 100 --questions 4 || echo "Demo data generation failed or already exists"

exec venv/bin/gunicorn -c ./consultation_analyser/gunicorn.py consultation_analyser.wsgi
