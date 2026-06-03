import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.harness.kernel_test_harness import KernelTestHarness


@pytest.fixture(scope="function")
def kernel_harness() -> KernelTestHarness:
    """
    Unified runtime-aware test harness.

    SINGLE SOURCE OF TRUTH FOR WHOLE TEST SUITE.
    """
    return KernelTestHarness()


@pytest.fixture(scope="function")
def kernel(kernel_harness: KernelTestHarness) -> RuntimeKernel:
    """Return runtime kernel facade."""
    return kernel_harness.kernel
