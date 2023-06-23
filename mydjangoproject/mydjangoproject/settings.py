import io
import os
from urllib.parse import urlparse
import environ
import structlog
# # Import structlog
from .logging_config import *

# Import the original settings from each template
from .basesettings import *

# Load the settings from the environment variable
env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))


# Setting this value from django-environ
SECRET_KEY = env("SECRET_KEY")

# If defined, add service URL to Django security settings
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
else:
    ALLOWED_HOSTS = ["*"]

# Default false. True allows default landing pages to be visible
DEBUG = env("DEBUG", default=False)

# Set this value from django-environ
DATABASES = {"default": env.db()}

# Change database settings if using the Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432


if "helloworld" not in INSTALLED_APPS:
     INSTALLED_APPS += ["helloworld"] 

# Static Files
if  "whitenoise.runserver_nostatic" not in INSTALLED_APPS:
     INSTALLED_APPS += [ "whitenoise.runserver_nostatic"] 

if  "whitenoise.middleware.WhiteNoiseMiddleware" not in MIDDLEWARE:
     MIDDLEWARE += [ "whitenoise.middleware.WhiteNoiseMiddleware"] 


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_URL = 'static/'
# STATICFILES_DIRS = [str(BASE_DIR.joinpath('static'))]
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# IF using Google Cloud Storage for static files:
# # Define static storage via django-storages[google]
# GS_BUCKET_NAME = env("GS_BUCKET_NAME")
# STATICFILES_DIRS = []
# DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
# GS_DEFAULT_ACL = "publicRead"


# # Add structured logging 
# LOGS_DIR = os.path.join(BASE_DIR, "logs")

# # Create logs directory if it doesn't exist
# if not os.path.exists(LOGS_DIR):
#     os.makedirs(LOGS_DIR)

# if  "django_structlog.middlewares.RequestMiddleware" not in MIDDLEWARE:
#      MIDDLEWARE += [ "django_structlog.middlewares.RequestMiddleware"]

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "json_formatter": {
#             "()": structlog.stdlib.ProcessorFormatter,
#             "processor": structlog.processors.JSONRenderer(),
#         },
#         "plain_console": {
#             "()": structlog.stdlib.ProcessorFormatter,
#             "processor": structlog.dev.ConsoleRenderer(),
#         },
#         "key_value": {
#             "()": structlog.stdlib.ProcessorFormatter,
#             "processor": structlog.processors.KeyValueRenderer(key_order=['timestamp', 'level', 'event', 'logger']),
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "plain_console",
#         },
#         "json_file": {
#             "class": "logging.handlers.WatchedFileHandler",
#             "filename": os.path.join(LOGS_DIR, "json.log"),
#             "formatter": "json_formatter",
#         },
#         "flat_line_file": {
#             "class": "logging.handlers.WatchedFileHandler",
#             "filename": os.path.join(LOGS_DIR, "flat_line.log"),
#             "formatter": "key_value",
#         },
#     },
#     "loggers": {
#         "django_structlog": {     
#             "handlers": ["console", "flat_line_file", "json_file"],
#             "level": "INFO",
#         },
#         # Make sure to replace the following logger's name for yours
#         "django_structlog_hello_django_project": {             
#             "handlers": ["console", "flat_line_file", "json_file"],
#             "level": "INFO",
#         },
#     }
# }

# structlog.configure(
#     processors=[
#         structlog.contextvars.merge_contextvars,
#         structlog.stdlib.filter_by_level,
#         structlog.processors.TimeStamper(fmt="iso"),
#         structlog.stdlib.add_logger_name,
#         structlog.stdlib.add_log_level,
#         structlog.stdlib.PositionalArgumentsFormatter(),
#         structlog.processors.StackInfoRenderer(),
#         structlog.processors.format_exc_info,
#         structlog.processors.UnicodeDecoder(),
#         structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
#     ],
#     logger_factory=structlog.stdlib.LoggerFactory(),
#     cache_logger_on_first_use=True,
# )
