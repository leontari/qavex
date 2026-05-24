from tests.factories.kernel import build_kernel_no_transport


def test_kernel_boots_without_http() -> None:
    kernel = build_kernel_no_transport()

    assert kernel is not None
