from __future__ import annotations

from unittest.mock import patch

from template_app.main import main


@patch("uvicorn.run")
def test_main_runs_uvicorn(mock_run) -> None:
    main()

    mock_run.assert_called_once_with(
        "template_app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_config=None,
    )
