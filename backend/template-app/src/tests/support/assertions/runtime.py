from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def assert_runtime_started(harness: KernelTestHarness) -> None:
    """
    Assert runtime startup completed.
    """
    assert harness.kernel is not None
