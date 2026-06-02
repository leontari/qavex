from __future__ import annotations

from unittest.mock import patch

from template_app.main_ import main


@patch("template_app.main_.uvicorn.run")
def test_main_dev_runs_uvicorn(mock_run) -> None:
    main()

    mock_run.assert_called_once_with(
        "template_app.asgi:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=None,
    )
