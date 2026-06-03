from __future__ import annotations

from unittest.mock import AsyncMock, Mock

from template_app.launcher.config import LauncherConfig
from template_app.runtime.transports.cli import entrypoint

from template_app.runtime.transports.cli.entrypoint import run_cli_runtime


# def test_cli_entrypoint_executes(monkeypatch) -> None:
#     kernel = Mock()
#
#     monkeypatch.setattr(
#         "template_app.runtime.transports.cli.entrypoint.build_cli_parser",
#         lambda: Mock(parse_args=lambda: Mock(version=False)),
#     )
#
#     monkeypatch.setattr(
#         "template_app.runtime.transports.cli.entrypoint.CLITransport",
#         lambda: Mock(),
#     )
#
#     run_cli_runtime(kernel)
#
#     kernel.install_transport.assert_called()
#     kernel.startup.assert_called()


def test_cli_entrypoint_runs_kernel_startup(monkeypatch) -> None:
    kernel = Mock()
    kernel.startup = AsyncMock()

    def fake_run(coro):
        import asyncio
        asyncio.new_event_loop().run_until_complete(coro)

    monkeypatch.setattr(
        entrypoint.asyncio,
        "run",
        fake_run,
    )

    entrypoint.run_cli_runtime(
        kernel=kernel,
        config=LauncherConfig(),
    )

    kernel.startup.assert_awaited_once()
