from __future__ import annotations

import pytest

from template_app.launcher.modes import LaunchMode


########################
# parsing functionality
########################


def test_from_string_parses_http() -> None:
    mode = LaunchMode.from_string(
        "http",
    )

    assert mode is LaunchMode.HTTP


def test_from_string_is_case_insensitive() -> None:
    mode = LaunchMode.from_string(
        "KaFkA",
    )

    assert mode is LaunchMode.KAFKA


def test_from_string_strips_whitespace() -> None:
    mode = LaunchMode.from_string(
        " grpc ",
    )

    assert mode is LaunchMode.GRPC


def test_from_string_raises_on_invalid_mode() -> None:
    with pytest.raises(ValueError):
        LaunchMode.from_string(
            "invalid",
        )


########################
# values functionality
########################


def test_values_returns_all_modes() -> None:
    values = LaunchMode.values()

    assert values == (
        "http",
        "kafka",
        "grpc",
        "cli",
    )


########################
# runtime classification
########################


def test_http_is_network_service() -> None:
    assert LaunchMode.HTTP.is_network_service is True


def test_grpc_is_network_service() -> None:
    assert LaunchMode.GRPC.is_network_service is True


def test_kafka_is_not_network_service() -> None:
    assert LaunchMode.KAFKA.is_network_service is False


def test_cli_is_not_network_service() -> None:
    assert LaunchMode.CLI.is_network_service is False


def test_kafka_is_background_worker() -> None:
    assert LaunchMode.KAFKA.is_background_worker is True


def test_http_is_not_background_worker() -> None:
    assert LaunchMode.HTTP.is_background_worker is False


def test_cli_is_interactive() -> None:
    assert LaunchMode.CLI.is_interactive is True


def test_http_is_not_interactive() -> None:
    assert LaunchMode.HTTP.is_interactive is False


#########################
# orchestration semantics
#########################


def test_http_requires_readiness() -> None:
    assert LaunchMode.HTTP.requires_readiness is True


def test_kafka_requires_readiness() -> None:
    assert LaunchMode.KAFKA.requires_readiness is True


def test_cli_does_not_require_readiness() -> None:
    assert LaunchMode.CLI.requires_readiness is False


def test_http_supports_graceful_shutdown() -> None:
    assert LaunchMode.HTTP.supports_graceful_shutdown is True


def test_cli_does_not_support_graceful_shutdown() -> None:
    assert LaunchMode.CLI.supports_graceful_shutdown is False


def test_http_requires_transport_runtime() -> None:
    assert LaunchMode.HTTP.requires_transport_runtime is True


def test_kafka_requires_transport_runtime() -> None:
    assert LaunchMode.KAFKA.requires_transport_runtime is True


def test_grpc_requires_transport_runtime() -> None:
    assert LaunchMode.GRPC.requires_transport_runtime is True


def test_cli_does_not_require_transport_runtime() -> None:
    assert LaunchMode.CLI.requires_transport_runtime is False


#########################
# kubernetes integration
#########################


def test_http_supports_horizontal_scaling() -> None:
    assert LaunchMode.HTTP.supports_horizontal_scaling is True


def test_kafka_supports_horizontal_scaling() -> None:
    assert LaunchMode.KAFKA.supports_horizontal_scaling is True


def test_grpc_supports_horizontal_scaling() -> None:
    assert LaunchMode.GRPC.supports_horizontal_scaling is True


def test_cli_does_not_support_horizontal_scaling() -> None:
    assert LaunchMode.CLI.supports_horizontal_scaling is False


def test_http_supports_probes() -> None:
    assert LaunchMode.HTTP.supports_probes is True


def test_kafka_supports_probes() -> None:
    assert LaunchMode.KAFKA.supports_probes is True


def test_grpc_supports_probes() -> None:
    assert LaunchMode.GRPC.supports_probes is True


def test_cli_does_not_support_probes() -> None:
    assert LaunchMode.CLI.supports_probes is False


def test_all_launch_modes_present() -> None:
    assert LaunchMode.HTTP
    assert LaunchMode.KAFKA
    assert LaunchMode.GRPC
    assert LaunchMode.CLI


def test_launch_mode_classification() -> None:
    assert LaunchMode.HTTP.is_http is True
    assert LaunchMode.KAFKA.is_worker is True
    assert LaunchMode.GRPC.is_network_transport is True
    assert LaunchMode.CLI.is_worker is True
