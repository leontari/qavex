from __future__ import annotations

from template_app.main import main


def test_main_runs_uvicorn(monkeypatch) -> None:
    """
    Local dev entrypoint must invoke uvicorn.
    """

    captured = {}

    def fake_run(*args, **kwargs):
        captured["args"] = args
        captured["kwargs"] = kwargs

    monkeypatch.setattr(
        "template_app.main.uvicorn.run",
        fake_run,
    )

    main()

    assert captured["args"][0] == "template_app:app"

    assert captured["kwargs"]["reload"] is True
