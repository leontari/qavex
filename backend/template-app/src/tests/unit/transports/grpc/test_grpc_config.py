from template_app.runtime.transports.grpc.config import GRPCTransportConfig


def test_grpc_config_defaults() -> None:
    cfg = GRPCTransportConfig()

    assert cfg.port == 50051
    assert cfg.host == "0.0.0.0"
