import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel
from tests.support.harness.kernel_test_client import KernelTestHarness


@pytest.fixture(scope="session")
def kernel_harness() -> KernelTestHarness:
    """
    Global runtime-aware harness.

    SINGLE SOURCE OF TRUTH FOR WHOLE TEST SUITE.
    """
    return KernelTestHarness()


@pytest.fixture
def kernel(kernel_harness: KernelTestHarness) -> RuntimeKernel:
    """Return runtime kernel facade."""
    return kernel_harness.kernel
