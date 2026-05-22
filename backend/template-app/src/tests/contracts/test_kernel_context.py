from __future__ import annotations

from fastapi import FastAPI

from template_app.bootstrap.runtime.bootstrap import bootstrap_application
from tests.factories.kernel import build_testing_kernel


def test_kernel_contains_application_context() -> None:
    kernel = build_testing_kernel()

    assert isinstance(kernel._context.app, FastAPI)


def test_kernel_contains_installed_modules() -> None:
    kernel = build_testing_kernel()

    assert len(kernel.modules) > 0
