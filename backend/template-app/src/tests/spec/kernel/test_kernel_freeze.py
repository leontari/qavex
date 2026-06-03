import pytest

from template_app.runtime.kernel.kernel import RuntimeKernel

from tests.support.fakes.transports import FakeTransport


def test_kernel_is_frozen_after_launcher_build(kernel: RuntimeKernel) -> None:
    assert kernel.is_frozen is True


def test_transport_installation_forbidden(kernel: RuntimeKernel) -> None:
    with pytest.raises(RuntimeError):
        kernel.install_transport(FakeTransport())
