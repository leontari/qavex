from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_kernel_exposes_metadata(
    kernel_harness: KernelTestHarness,
) -> None:
    assert kernel_harness.kernel.metadata is not None


def test_kernel_exposes_capabilities(
    kernel_harness: KernelTestHarness,
) -> None:
    assert (
        kernel_harness.kernel.capabilities
        is kernel_harness.kernel.metadata.capabilities
    )


def test_kernel_exposes_descriptor(
    kernel_harness: KernelTestHarness,
) -> None:
    assert (
        kernel_harness.kernel.descriptor
        is kernel_harness.kernel.metadata.descriptor
    )
