from unittest.mock import Mock

from template_app.runtime.transports.grpc.entrypoint import run_grpc_runtime


def test_grpc_entrypoint_executes(monkeypatch) -> None:
    kernel = Mock()

    monkeypatch.setattr(
        "template_app.transports.grpc.transport.GRPCTransport",
        lambda: Mock(),
    )

    run_grpc_runtime(kernel)

    kernel.install_transport.assert_called()
    kernel.startup.assert_called()
