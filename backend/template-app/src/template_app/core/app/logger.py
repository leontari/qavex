from __future__ import annotations

import logging
import logging.config
from pathlib import Path

import yaml

LEVEL_COLORS = {
    "DEBUG": "\033[34m",  # blue
    "INFO": "\033[32m",  # green
    "WARNING": "\033[33m",  # yellow
    "ERROR": "\033[31m",  # red
    "CRITICAL": "\033[1;31m",  # bright red
}

COLUMN_COLORS = {
    "time": "\033[36m",  # cyan
    "logger": "\033[35m",  # magenta
    "lineno": "\033[90m",  # gray
    "reset": "\033[0m",
}

ACCESS_COLORS = {
    "client": "\033[36m",  # cyan
    "method": "\033[33m",  # yellow
    "path": "\033[32m",  # green
    "status_2xx": "\033[32m",  # green
    "status_3xx": "\033[33m",  # yellow
    "status_4xx": "\033[31m",  # red
    "status_5xx": "\033[1;31m",
    "reset": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    def format(self, record):
        # Цвет уровня
        record.levelname_color = LEVEL_COLORS.get(record.levelname, "")

        # Цвет времени
        record.time_color = COLUMN_COLORS["time"]

        # Цвет логгера
        record.logger_color = COLUMN_COLORS["logger"]

        # Цвет номера строки
        record.lineno_color = COLUMN_COLORS["lineno"]

        # Сброс
        record.reset = COLUMN_COLORS["reset"]

        return super().format(record)


class UvicornAccessFormatter(logging.Formatter):
    def format(self, record):
        msg = record.getMessage()

        # Пример строки:
        # 127.0.0.1:54321 - "GET / HTTP/1.1" 200 OK

        try:
            client, rest = msg.split(" - ", 1)
            request, status = rest.rsplit(" ", 1)
        except ValueError:
            return msg  # fallback

        method = request.split(" ")[0].replace('"', "")
        path = request.split(" ")[1]

        status_code = int(status)

        if 200 <= status_code < 300:
            status_color = ACCESS_COLORS["status_2xx"]
        elif 300 <= status_code < 400:
            status_color = ACCESS_COLORS["status_3xx"]
        elif 400 <= status_code < 500:
            status_color = ACCESS_COLORS["status_4xx"]
        else:
            status_color = ACCESS_COLORS["status_5xx"]

        record.client_color = ACCESS_COLORS["client"]
        record.method_color = ACCESS_COLORS["method"]
        record.path_color = ACCESS_COLORS["path"]
        record.status_color = status_color
        record.reset = ACCESS_COLORS["reset"]

        record.client = client
        record.method = method
        record.path = path
        record.status = status_code

        return super().format(record)


def setup_logging() -> None:
    """Load logging configuration from YAML file."""
    base_dir = Path(__file__).resolve().parent.parent  # template_app/
    print(base_dir)
    config_path = base_dir / "config" / "logging.yaml"
    print(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Logging config not found: {config_path}")

    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
