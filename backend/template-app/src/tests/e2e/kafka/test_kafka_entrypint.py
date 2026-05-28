from template_app.kafka import main


def test_kafka_entrypoint_importable() -> None:
    assert main
