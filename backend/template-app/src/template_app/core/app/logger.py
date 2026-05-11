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


def list_all_loggers():
    logger_dict = logging.Logger.manager.loggerDict
    result = []
    for name, logger in logger_dict.items():
        if isinstance(logger, logging.Logger):
            handlers = [h.__class__.__name__ for h in logger.handlers]
            result.append((name, logging.getLevelName(logger.level), handlers))
    return result


#
# for name, level, handlers in list_all_loggers():
#     print(f"{name:30} | level={level:8} | handlers={handlers}")


def setup_logging() -> None:
    """Load logging configuration from YAML file."""
    import os

    root = logging.getLogger()

    # если логирование уже настроено - ничего не делаем
    if root.hasHandlers():
        return

    env = os.getenv("APP_ENV", "dev").lower()
    config_name = "logger.prod.yaml" if env == "prod" else "logger.dev.yaml"

    base_dir = Path(__file__).resolve().parent.parent.parent  # template_app/
    config_path = base_dir / "config" / config_name

    if not config_path.exists():
        msg = f"Logging config not found: {config_path}"
        raise FileNotFoundError(msg)

    with Path(config_path).open("r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config)
