from tests.factories.kernel import build_testing_kernel
from tests.factories.transport import get_http_app


def test_runtime_not_stored_in_fastapi_state() -> None:
    kernel = build_testing_kernel()

    app = get_http_app(kernel)

    assert not hasattr(app.state, "runtime")
    assert not hasattr(app.state, "kernel")
    assert not hasattr(app.state, "context")
