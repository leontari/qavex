import pytest

from tests.support.fakes.transports import (
    FakeTransport,
)
from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_runtime_graph_is_frozen_after_bootstrap(
    kernel_harness: KernelTestHarness,
) -> None:
    assert kernel_harness.kernel.freeze.frozen is True


def test_install_transport_after_freeze_fails(
    kernel_harness: KernelTestHarness,
) -> None:
    with pytest.raises(RuntimeError):
        kernel_harness.kernel.install_transport(
            FakeTransport(),
        )
