from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_context_owns_runtime(
    kernel_harness: KernelTestHarness,
) -> None:
    assert (
        kernel_harness.kernel.context.runtime
        is kernel_harness.kernel.runtime
    )


def test_context_owns_metadata(
    kernel_harness: KernelTestHarness,
) -> None:
    assert (
        kernel_harness.kernel.context.metadata
        is kernel_harness.kernel.metadata
    )
