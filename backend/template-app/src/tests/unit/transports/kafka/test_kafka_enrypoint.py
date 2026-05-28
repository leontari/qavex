from unittest.mock import Mock

from template_app.transports.kafka.entrypoint import run_kafka_runtime


def test_kafka_entrypoint_executes(monkeypatch) -> None:
    kernel = Mock()

    monkeypatch.setattr(
        "template_app.transports.kafka.entrypoint.KafkaTransport",
        lambda: Mock(),
    )

    run_kafka_runtime(kernel)

    kernel.install_transport.assert_called()
    kernel.startup.assert_called()
