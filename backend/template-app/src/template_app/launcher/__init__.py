"""Launcher public API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from template_app.launcher.config import LauncherConfig
from template_app.launcher.modes import LaunchMode
from template_app.launcher.run import KernelLauncher

if TYPE_CHECKING:
    from fastapi import FastAPI


def build_http_app() -> FastAPI:
    """
    Build ASGI application.

    Used only by asgi.py.

    Returns:
        FastAPI instance for external runners

    """
    launcher = KernelLauncher(LauncherConfig(mode=LaunchMode.HTTP))

    return launcher.build_http_app()


def run_http() -> None:
    """Run HTTP runtime."""
    KernelLauncher(LauncherConfig(mode=LaunchMode.HTTP)).run()


def run_grpc() -> None:
    """Run gRPC runtime."""
    KernelLauncher(LauncherConfig(mode=LaunchMode.GRPC)).run()


def run_kafka() -> None:
    """Run Kafka runtime."""
    KernelLauncher(LauncherConfig(mode=LaunchMode.KAFKA)).run()


def run_cli() -> None:
    """Run CLI runtime."""
    KernelLauncher(LauncherConfig(mode=LaunchMode.CLI)).run()
