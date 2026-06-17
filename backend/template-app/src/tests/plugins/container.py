import pytest

from template_app.runtime.container.container import Container
from template_app.runtime.container.models.dependency import DependencyID
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.models.scope import (
    ScopeID, DependencyScope,
)
from template_app.runtime.container.models.visibility import (
    DependencyVisibility,
)
from template_app.runtime.container.providers import FactoryProvider
from template_app.runtime.container.runtime.helpers.context_manager import (
    ResolutionContextManager,
)
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope_manager import (
    ScopeManager,
)
from template_app.runtime.container.models.dependency import (
    DependencyDescriptor,
)
from template_app.runtime.container.runtime.singleton_cache import (
    SingletonCache,
)


class ServiceA: ...
class ServiceB: ...


@pytest.fixture
def namespace() -> Namespace:
    return Namespace(name="test")


@pytest.fixture
def dependency_id(namespace: Namespace) -> DependencyID:
    return DependencyID(
        namespace=namespace,
        contract=ServiceA,
    )

@pytest.fixture
def dependency_id_2(namespace: Namespace) -> DependencyID:
    return DependencyID(
        namespace=namespace,
        contract=ServiceB
    )


@pytest.fixture
def scope_id() -> ScopeID:
    return ScopeID.new()


@pytest.fixture
def descriptor(
    dependency_id: DependencyID,
) -> DependencyDescriptor:
    return DependencyDescriptor(
        ident=dependency_id,
        provider=FactoryProvider(ServiceA),
        scope=DependencyScope.TRANSIENT,
        visibility=DependencyVisibility.PUBLIC,
    )


@pytest.fixture
def registry() -> DependencyRegistry:
    return DependencyRegistry()


@pytest.fixture
def context_manager():
    return ResolutionContextManager()


@pytest.fixture
def scope_manager():
    return ScopeManager()


@pytest.fixture
def container():
    return Container()


@pytest.fixture
def scope_context(scope_manager):
    scope_id = scope_manager.create_scope()
    return scope_manager.get_scope(scope_id)


@pytest.fixture
def singleton_cache():
    return SingletonCache()
