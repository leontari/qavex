from template_app.runtime.transports.http.config import HTTPTransportConfig


def test_http_config_defaults() -> None:
    cfg = HTTPTransportConfig()

    assert cfg.host == "127.0.0.1"
    assert cfg.port == 8000
    assert cfg.reload is False
