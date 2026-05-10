from __future__ import annotations

import logging

from template_app.core.app.logger import ColorFormatter


def test_color_formatter(caplog):
    logger = logging.getLogger("template_app")
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter("%(levelname_color)s%(levelname)s%(reset)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    with caplog.at_level(logging.INFO):
        logger.info("hello")

    assert "hello" in caplog.text


def test_color_formatter_basic(caplog):
    logger = logging.getLogger("template_app.test")
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter("%(levelname_color)s%(levelname)s%(reset)s %(message)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    with caplog.at_level(logging.INFO):
        logger.info("hello")

    text = caplog.text
    assert "hello" in text
    assert "INFO" in text
    assert "\033[" in text  # ANSI present


def test_color_formatter_alignment(caplog):
    fmt = "%(levelname)-8s %(name)-20s:%(lineno)-4d - %(message)s"
    handler = logging.StreamHandler()
    handler.setFormatter(ColorFormatter(fmt))

    logger = logging.getLogger("template_app.align")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    with caplog.at_level(logging.INFO):
        logger.info("short")
        logger.info("a bit longer message")

    lines = caplog.text.splitlines()
    assert len(lines) == 2
    assert lines[0].index("template_app.align") == lines[1].index(
        "template_app.align"
    )


def test_uvicorn_access_logger(caplog):
    logger = logging.getLogger("uvicorn.access")

    with caplog.at_level(logging.INFO):
        logger.info('127.0.0.1:1 - "GET / HTTP/1.1" 200 OK')

    text = caplog.text
    assert "GET" in text
    assert "200" in text
    assert "\033[" in text  # colored


def test_uvicorn_error_logger(caplog):
    logger = logging.getLogger("uvicorn.error")

    with caplog.at_level(logging.ERROR):
        logger.error("boom")

    assert "boom" in caplog.text
    assert "\033[" in caplog.text


def test_app_logger(caplog):
    logger = logging.getLogger("template_app")

    with caplog.at_level(logging.INFO):
        logger.info("hello app")

    assert "hello app" in caplog.text
    assert "\033[" in caplog.text
