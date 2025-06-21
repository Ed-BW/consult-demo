import sentry_sdk
from django.conf.global_settings import STORAGES

from consultation_analyser.settings.base import *  # noqa

# Handle DOMAIN_NAME gracefully
DOMAIN_NAME = env("DOMAIN_NAME", default="web-production-dbf3.up.railway.app")
CSRF_TRUSTED_ORIGINS = ["https://" + DOMAIN_NAME]

# Handle Sentry configuration gracefully
SENTRY_DSN = env("SENTRY_DSN", default="")
EXECUTION_CONTEXT = env("EXECUTION_CONTEXT", default="railway")
GIT_SHA = env("GIT_SHA", default="unknown")

# Handle S3 storage gracefully - only configure if APP_BUCKET is provided
APP_BUCKET = env("APP_BUCKET", default="")
if APP_BUCKET:
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {"bucket_name": APP_BUCKET, "location": "app_data/"},
    }
else:
    # Use local file storage if no S3 bucket is configured
    STORAGES["default"] = {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    }


def sentry_before_send(event, hint):
    """Filters Sentry events before sending.

    Adapted from https://jkfran.com/capturing-unhandled-exceptions-sentry-python/

    This function filters out handled exceptions.

    Args:
        event (dict): The event dictionary containing exception data.

        hint (dict): Additional information about the event, including
            the original exception.

    Returns:
        dict: The modified event dictionary, or None if the event should be
            ignored.
    """
    # Ignore handled exceptions
    exceptions = event.get("exception", {}).get("values", [])
    if exceptions:
        exc = exceptions[-1]
        mechanism = exc.get("mechanism")

        if mechanism:
            if mechanism.get("handled"):
                return None

    return event


# Only initialize Sentry if we have a valid DSN
if SENTRY_DSN and not SENTRY_DSN.startswith("dummy") and "dummy" not in SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        environment=ENVIRONMENT,  # noqa: F405
        release=GIT_SHA,
        before_send=sentry_before_send,
        traces_sample_rate=1.0,
        profile_session_sample_rate=1.0,
        profile_lifecycle="trace",
    )
    sentry_sdk.set_tags({"execution_context": EXECUTION_CONTEXT})
