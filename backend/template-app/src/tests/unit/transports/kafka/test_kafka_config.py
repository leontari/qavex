from template_app.runtime.transports.kafka.config import KafkaTransportConfig


def test_kafka_config_defaults() -> None:
    cfg = KafkaTransportConfig()

    assert cfg.bootstrap_servers
    assert cfg.consumer_group
