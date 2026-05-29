import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.infrastructure.runtime import InfrastructureRuntime
from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.kernel.runtime.state import RuntimeState
from template_app.runtime.lifecycle.runtime import LifecycleRuntime
from template_app.runtime.messaging.runtime import MessagingRuntime
from template_app.runtime.modules.runtime import ModuleRuntime
from template_app.runtime.transports.runtime import TransportRuntime


@pytest.fixture
def runtime(kernel: RuntimeKernel) -> RuntimeState:
    """Return runtime graph."""
    return kernel.runtime


@pytest.fixture
def container(runtime: RuntimeState) -> Container:
    return runtime.container


@pytest.fixture
def lifecycle(runtime: RuntimeState) -> LifecycleRuntime:
    return runtime.lifecycle


@pytest.fixture
def infrastructure(runtime: RuntimeState) -> InfrastructureRuntime:
    return runtime.infrastructure


@pytest.fixture
def messaging(runtime: RuntimeState) -> MessagingRuntime:
    return runtime.messaging


@pytest.fixture
def transports(runtime: RuntimeState) -> TransportRuntime:
    return runtime.transports


@pytest.fixture
def modules(runtime: RuntimeState) -> ModuleRuntime:
    return runtime.modules
