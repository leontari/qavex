from tests.support.harness.kernel_test_client import KernelTestClient


def test_kernel_created(client: KernelTestClient) -> None:
    assert client.kernel is not None


def test_runtime_created(client: KernelTestClient) -> None:
    assert client.runtime is not None


def test_kernel_contains_context(client: KernelTestClient) -> None:
    assert client.kernel.context is not None
