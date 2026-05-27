"""Kafka transport configuration."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class KafkaTransportConfig:
    """
    Kafka transport configuration.

    Responsibilities:
        - broker configuration
        - consumer tuning
        - retry tuning
    """

    bootstrap_servers: str = "localhost:9092"

    consumer_group: str = "template-app"

    auto_offset_reset: str = "earliest"

    enable_auto_commit: bool = True
