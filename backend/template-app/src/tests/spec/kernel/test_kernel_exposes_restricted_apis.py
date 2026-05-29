from template_app.runtime.kernel.bootstrap import (
    bootstrap_kernel,
)
from template_app.runtime.modules.apis import (
    ModuleInfraAPI,
    ModuleMessagingAPI,
    ModuleRuntimeAPI,
)


def test_kernel_creates_runtime_api() -> None:
    kernel = bootstrap_kernel()

    api = kernel.create_runtime_api()

    assert isinstance(
        api,
        ModuleRuntimeAPI,
    )


def test_kernel_creates_infrastructure_api() -> None:
    kernel = bootstrap_kernel()

    api = kernel.create_infra_api()

    assert isinstance(
        api,
        ModuleInfraAPI,
    )


def test_kernel_creates_messaging_api() -> None:
    kernel = bootstrap_kernel()

    api = kernel.create_messaging_api()

    assert isinstance(
        api,
        ModuleMessagingAPI,
    )
