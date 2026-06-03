from __future__ import annotations

from template_app.main_ import main


def test_main_dev_runs_uvicorn(monkeypatch) -> None:
    captured = {}

    def fake_run(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

    monkeypatch.setattr(
        "template_app.main_.uvicorn.run",
        fake_run,
    )

    main()

    assert captured["args"][0] == "template_app.asgi:app"

    assert captured["kwargs"]["reload"] is True

    assert captured["kwargs"]["host"] == "127.0.0.1"

    assert captured["kwargs"]["port"] == 8000
