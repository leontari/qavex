# tests/contracts/test_launch_modes.py

from __future__ import annotations

import pytest

from template_app.launcher.modes import LaunchMode


def test_all_launch_modes_present() -> None:
    assert LaunchMode.HTTP
    assert LaunchMode.KAFKA
    assert LaunchMode.GRPC
    assert LaunchMode.CLI


def test_launch_mode_values() -> None:
    assert LaunchMode.HTTP.value == "http"
    assert LaunchMode.KAFKA.value == "kafka"
    assert LaunchMode.GRPC.value == "grpc"
    assert LaunchMode.CLI.value == "cli"


def test_launch_mode_from_string() -> None:
    assert LaunchMode.from_string("http") is LaunchMode.HTTP
    assert LaunchMode.from_string("KAFKA") is LaunchMode.KAFKA
    assert LaunchMode.from_string("grpc") is LaunchMode.GRPC
    assert LaunchMode.from_string("cli") is LaunchMode.CLI


def test_launch_mode_invalid() -> None:
    with pytest.raises(ValueError):
        LaunchMode.from_string("invalid")


def test_http_mode_features() -> None:
    mode = LaunchMode.HTTP

    assert mode.supports_http is True
    assert mode.is_network_transport is True
    assert mode.is_worker is False


def test_kafka_mode_features() -> None:
    mode = LaunchMode.KAFKA

    assert mode.supports_kafka is True
    assert mode.is_worker is True
    assert mode.is_network_transport is False


def test_grpc_mode_features() -> None:
    mode = LaunchMode.GRPC

    assert mode.supports_grpc is True
    assert mode.is_network_transport is True


def test_cli_mode_features() -> None:
    mode = LaunchMode.CLI

    assert mode.supports_cli is True
    assert mode.is_interactive is True


def test_launch_mode_values_helper() -> None:
    assert LaunchMode.values() == (
        "http",
        "kafka",
        "grpc",
        "cli",
    )
