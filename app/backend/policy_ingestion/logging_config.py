import logging
import sys

import structlog


def setup_logging(dev: bool = True):
    timestamper = structlog.processors.TimeStamper(fmt="iso")

    shared_processors = [
        structlog.processors.add_log_level,
        timestamper,
    ]

    if dev:
        processors = shared_processors + [structlog.dev.ConsoleRenderer()]
    else:
        processors = shared_processors + [structlog.processors.JSONRenderer()]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        cache_logger_on_first_use=True,
    )
