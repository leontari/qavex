"""
Kafka runtime settings.

This module contains environment-driven Apache Kafka configuration
used for asynchronous messaging and event-driven communication.

The settings defined here control:
- Kafka broker connectivity
- consumer group configuration
- topic defaults
- producer behavior
- transport security
- authentication settings

Supported deployment targets:
- local development
- automated testing
- CI pipelines
- Docker containers
- Kubernetes clusters
- bare-metal installations

Configuration sources:
- environment variables
- .env files
- Docker/Kubernetes secrets
- CI/CD runtime injection

Typical Kafka use cases:
- event-driven architecture
- asynchronous task processing
- microservice communication
- audit/event streams
- analytics pipelines
- stream processing

Security considerations:
    Production Kafka clusters should:
    - require authentication
    - use TLS encryption
    - restrict broker network exposure
    - isolate internal traffic

Example:
    KAFKA_BOOTSTRAP_SERVERS=kafka:9092

Design principles:
    - strict typing
    - immutable runtime configuration
    - deployment portability
    - infrastructure isolation
    - cloud-native compatibility
"""

from __future__ import annotations

from pydantic import Field
from pydantic_settings import BaseSettings

from template_app.config_.settings.common import (
    COMMON_SETTINGS_CONFIG,
)


class KafkaSettings(BaseSettings):
    """
    Runtime Apache Kafka configuration.

    This settings model defines Kafka connectivity and messaging
    runtime configuration used by producers and consumers.

    Attributes:
        KAFKA_ENABLED:
            Enables Kafka integration.

        KAFKA_BOOTSTRAP_SERVERS:
            List of Kafka bootstrap broker addresses.

        KAFKA_CLIENT_ID:
            Kafka client identifier.

        KAFKA_GROUP_ID:
            Default Kafka consumer group identifier.

        KAFKA_SECURITY_PROTOCOL:
            Kafka transport security protocol.

        KAFKA_SASL_MECHANISM:
            SASL authentication mechanism.

        KAFKA_SASL_USERNAME:
            SASL authentication username.

        KAFKA_SASL_PASSWORD:
            SASL authentication password.

        KAFKA_DEFAULT_TOPIC:
            Default Kafka topic name.
    """

    KAFKA_ENABLED: bool = False

    KAFKA_BOOTSTRAP_SERVERS: list[str] = Field(
        default=["localhost:9092"],
    )

    KAFKA_CLIENT_ID: str = "template-app"

    KAFKA_GROUP_ID: str = "template-app-group"

    KAFKA_SECURITY_PROTOCOL: str = "PLAINTEXT"

    KAFKA_SASL_MECHANISM: str | None = None

    KAFKA_SASL_USERNAME: str | None = None

    KAFKA_SASL_PASSWORD: str | None = None

    KAFKA_DEFAULT_TOPIC: str = "template-app-events"

    model_config = COMMON_SETTINGS_CONFIG
