import os

workers = os.environ.get("GUNICORN_WORKERS")
port = os.environ.get("PORT", "8000")
bind = f"0.0.0.0:{port}"
accesslog = "-"
errorlog = "-"
timeout = os.environ.get("GUNICORN_TIMEOUT")
