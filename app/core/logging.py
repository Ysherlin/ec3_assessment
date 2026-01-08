import logging
import sys
from typing import Optional


def configure_logging(log_level: str = "INFO") -> None:
    """
    Configure application logging.

    - Logs to stdout (works well for local dev + containers).
    - Uses a consistent format with timestamps and logger names.
    - Also normalizes uvicorn loggers so everything looks consistent.
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    root = logging.getLogger()
    root.setLevel(level)

    # Remove any existing handlers (avoid duplicated logs when reload runs)
    for h in list(root.handlers):
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    root.addHandler(handler)

    # Ensure uvicorn loggers follow the same level and handlers
    for logger_name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(logger_name)
        logger.handlers = []
        logger.propagate = True
        logger.setLevel(level)
