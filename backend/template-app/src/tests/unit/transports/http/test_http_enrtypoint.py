from unittest.mock import Mock

from template_app.runtime.transports.http.entrypoint import run_http_runtime


def test_http_entrypoint_executes(monkeypatch) -> None:
    kernel = Mock()
    config = Mock()

    monkeypatch.setattr(
        "template_app.runtime.transports.http.entrypoint.create_http_app",
        lambda k: Mock(),
    )

    monkeypatch.setattr(
        "template_app.runtime.transports.http.entrypoint.FastAPITransport",
        lambda app: Mock(),
    )

    monkeypatch.setattr(
        "template_app.runtime.transports.http.entrypoint.uvicorn.run",
        lambda *a, **kw: None,
    )

    run_http_runtime(kernel, config)

    kernel.install_transport.assert_called()
