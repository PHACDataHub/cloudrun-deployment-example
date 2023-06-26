# https://www.structlog.org/en/stable/
import os
import structlog
import logging.config
from google.cloud import logging as google_logging
logging.basicConfig(level=logging.INFO)

# Configure structlog

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
    # level=logging.INFO 
)


# Configure the root logger conditionally for GCP environment
if 'GOOGLE_CLOUD_PROJECT' in os.environ:
    client = google_logging.Client()
    handler = google_logging.handlers.CloudLoggingHandler(client)
    formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer()
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.DEBUG)

