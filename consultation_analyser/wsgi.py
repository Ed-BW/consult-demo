"""
WSGI config for consultation_analyser project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Use production settings by default, but allow override via environment variable
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "consultation_analyser.settings.production")

application = get_wsgi_application()
