"""
Application logging configuration and custom formatters.

This module provides:

- ANSI color definitions for terminal logging output.
- Custom logging formatters for standard application logs.
- Utility functions for inspecting registered loggers.
- Centralized logging configuration loading from YAML files.

"""

from __future__ import annotations

import logging
import logging.config
import os
import sys
import tomllib
from enum import IntEnum
from pathlib import Path

###########################
# ANSI COLORS
###########################


# ANSI colors for log levels.
LEVEL_COLORS = {
    "DEBUG": "\033[34m",  # blue
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # red
}

# ANSI colors for common log columns.
COLUMN_COLORS = {
    "time": "\033[36m",  # cyan
    "logger": "\033[35m",  # magenta
    "lineno": "\033[90m",  # gray
    "reset": "\033[0m",
}

# ANSI colors for HTTP access logs.
ACCESS_COLORS = {
    "client": "\033[36m",  # cyan
    "method": "\033[33m",  # yellow
    "path": "\033[32m",  # green
    "status_1xx": "\033[36m",  # cyan
    "status_2xx": "\033[32m",  # green
    "status_3xx": "\033[33m",  # yellow
    "status_4xx": "\033[31m",  # red
    "status_5xx": "\033[1;31m",  # red
    "reset": "\033[0m",
}


###########################
# HTTP STATUS
###########################


class HTTPStatusClass(IntEnum):
    """HTTP status code classes (Starlette-style grouping)."""

    INFORMATIONAL = 1
    SUCCESS = 2
    REDIRECTION = 3
    CLIENT_ERROR = 4
    SERVER_ERROR = 5

    @classmethod
    def from_code(cls, code: int) -> HTTPStatusClass:
        """
        Convert HTTP status code to HTTP status class.

        Args:
            code: HTTP status code (e.g. 200, 404, 500).

        Returns:
            HTTPStatusClass: Corresponding status class.

        """
        return cls(code // 100)


STATUS_COLOR_MAP = {
    HTTPStatusClass.INFORMATIONAL: ACCESS_COLORS["status_1xx"],
    HTTPStatusClass.SUCCESS: ACCESS_COLORS["status_2xx"],
    HTTPStatusClass.REDIRECTION: ACCESS_COLORS["status_3xx"],
    HTTPStatusClass.CLIENT_ERROR: ACCESS_COLORS["status_4xx"],
    HTTPStatusClass.SERVER_ERROR: ACCESS_COLORS["status_5xx"],
}


def parse_access_message(msg: str) -> tuple[str, str, str, int] | None:
    """
    Parse uvicorn access log line.

    Returns:
        (client, method, path, status_code) or None

    """
    try:
        client, rest = msg.split(" - ", 1)
        request, status = rest.rsplit(" ", 1)

        method = request.split()[0].replace('"', "")
        path = request.split()[1]

        return client, method, path, int(status)
    except (ValueError, IndexError):
        return None


def get_status_color(code: int) -> str:
    """
    Return ANSI color for HTTP status code.

    Args:
        code: HTTP status code (e.g. 200, 404, 500).

    Returns:
        str: ANSI escape sequence representing status color.

    """
    try:
        status_class = HTTPStatusClass.from_code(code)
    except ValueError:
        return ACCESS_COLORS["status_5xx"]

    return STATUS_COLOR_MAP.get(status_class, ACCESS_COLORS["status_5xx"])


###########################
# FORMATTERS
###########################


class ColorFormatter(logging.Formatter):
    """
    Logging formatter with ANSI color support.

    Renders colored log records.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log record with ANSI colors.

        Args:
            record: Log record instance.

        Returns:
            str: Formatted log message.

        """
        # Color for log level
        record.levelname_color = LEVEL_COLORS.get(record.levelname, "")
        # Color for timestamp
        record.time_color = COLUMN_COLORS["time"]
        # Color for logger name
        record.logger_color = COLUMN_COLORS["logger"]
        # Color for line number
        record.lineno_color = COLUMN_COLORS["lineno"]
        # ANSI reset sequence
        record.reset = COLUMN_COLORS["reset"]
        return super().format(record)


class UvicornAccessFormatter(logging.Formatter):
    """
    Formatter for uvicorn access logs with ANSI colors.

    Renders parsed uvicorn HTTP access logs with applied colors
    base on request method and response status code.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format uvicorn access log record with ANSI colors.

        Args:
            record: Logging record instance.

        Returns:
            str: Colored and formatted log message.

        """
        # uvicorn.access log message example:
        # 127.0.0.1:54321 - "GET / HTTP/1.1" 200 OK
        parsed = parse_access_message(record.getMessage())

        if not parsed:
            return super().format(record)

        client_addr, method, path, status_code = parsed

        # shared fields
        record.levelname_color = LEVEL_COLORS.get(record.levelname, "")
        record.time_color = COLUMN_COLORS["time"]
        record.logger_color = COLUMN_COLORS["logger"]
        record.lineno_color = COLUMN_COLORS["lineno"]

        # access fields
        record.client_color = ACCESS_COLORS["client"]
        record.method_color = ACCESS_COLORS["method"]
        record.path_color = ACCESS_COLORS["path"]
        record.status_color = get_status_color(status_code)
        record.reset = ACCESS_COLORS["reset"]

        # values
        record.client = client_addr
        record.method = method
        record.path = path
        record.status = status_code

        return super().format(record)


###########################
# LOGGER UTILITIES
###########################


def list_all_loggers() -> list[tuple[str, str, list[str]]]:
    """
    Collect information about all registered loggers.

    Returns:
        list[tuple[str, str, list[str]]]:
            A list containing:

            - logger name
            - logger level
            - attached handler class names

    """
    logger_dict = logging.Logger.manager.loggerDict
    result = []
    for name, logger in logger_dict.items():
        if isinstance(logger, logging.Logger):
            handlers = [h.__class__.__name__ for h in logger.handlers]
            result.append((name, logging.getLevelName(logger.level), handlers))
    return result


def print_all_loggers() -> None:
    """Print all registered logger to stdout."""
    data = list_all_loggers()

    # table header
    header = f"{'LOGGER':30} | {'LEVEL':10} | HANDLERS"
    sys.stdout.write(header + "\n")
    sys.stdout.write("-" * len(header) + "\n")

    for name, level, handlers in data:
        handlers_str = ",".join(handlers) if handlers else "-"
        line = f"{name:30} | {level:10} | {handlers_str}"
        sys.stdout.write(line + "\n")


###########################
# SETUP LOGGING
###########################


def setup_logging() -> None:
    """Load logging configuration from TOML file."""
    env = os.getenv("APP_ENV", "dev").lower()

    config_name = "logger.prod.toml" if env == "prod" else "logger.dev.toml"

    base_dir = Path(__file__).resolve().parent.parent.parent
    config_path = base_dir / "config" / "logging" / config_name

    if not config_path.exists():
        msg = f"Logging config not found: {config_path}"
        raise FileNotFoundError(msg)

    with config_path.open("rb") as f:
        config = tomllib.load(f)

    logging.config.dictConfig(config)
