from __future__ import annotations


def test_color_formatter():
    logger = logging.getLogger("template_app.test")
    handler = logging.StreamHandler()
    handler.setFormatter(
        ColorFormatter("%(levelname_color)s%(levelname)s%(reset)s")
    )
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    with capsys.disabled():
        logger.info("hello")


def test_app_logger(caplog):
    logger = logging.getLogger("template_app")
    with caplog.at_level(logging.INFO):
        logger.info("hello")

    assert "hello" in caplog.text
