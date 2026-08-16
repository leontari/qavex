import pytest

from template_app.runtime.container import Container, DependencyProvider
from template_app.runtime.container.runtime.dependency import DependencyID
from template_app.runtime.container import (
    Namespace,
    DependencyScope,
    DependencyVisibility,
)
from template_app.runtime.container.runtime.scope.scope import ScopeID
from template_app.runtime.container.providers import FactoryProvider
from template_app.runtime.container.runtime.resolution import ResolutionManager
from template_app.runtime.container.runtime.registry import DependencyRegistry
from template_app.runtime.container.runtime.scope import ScopeManager
from template_app.runtime.container.runtime.dependency import (
    DependencyDescriptor,
)
from template_app.runtime.container.runtime.singleton import SingletonCache
from tests.support.fakes.providers import FakeStringProvider


class ServiceA: ...
class ServiceB: ...


@pytest.fixture
def namespace_a() -> Namespace:
    return Namespace(name="module.a")


@pytest.fixture
def namespace_b() -> Namespace:
    return Namespace("module.b")


@pytest.fixture
def owner_namespace(namespace_a: Namespace) -> Namespace:
    return namespace_a


@pytest.fixture
def requester_namespace(namespace_b: Namespace) -> Namespace:
    return namespace_b


@pytest.fixture
def dependency_id(namespace_a: Namespace) -> DependencyID:
    return DependencyID(
        namespace=namespace_a,
        contract=ServiceA,
    )

@pytest.fixture
def dependency_id_2(namespace_b: Namespace) -> DependencyID:
    return DependencyID(
        namespace=namespace_b,
        contract=ServiceB
    )


@pytest.fixture
def dependency_a(dependency_id) -> DependencyID:
    return dependency_id


@pytest.fixture
def dependency_b(dependency_id_2) -> DependencyID:
    return dependency_id_2


@pytest.fixture
def scope_id() -> ScopeID:
    return ScopeID.new()


@pytest.fixture
def descriptor(dependency_id: DependencyID) -> DependencyDescriptor:
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
def context_manager() -> ResolutionManager:
    return ResolutionManager()


@pytest.fixture
def scope_manager() -> ScopeManager:
    return ScopeManager()


@pytest.fixture
def container() -> Container:
    return Container()


@pytest.fixture
def scope_context(scope_manager):
    scope_id = scope_manager.create_scope()
    return scope_manager.get_scope(scope_id)


@pytest.fixture
def singleton_cache() -> SingletonCache:
    return SingletonCache()


@pytest.fixture
def fake_string_provider() -> DependencyProvider[str]:
    return FakeStringProvider
