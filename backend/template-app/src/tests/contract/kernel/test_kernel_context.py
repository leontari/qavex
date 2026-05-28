from __future__ import annotations

from tests.support.factories.kernel import build_testing_kernel


def test_kernel_contains_installed_modules() -> None:
    kernel = build_testing_kernel()

    assert len(kernel.modules) > 0
