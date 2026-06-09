import pytest

from template_app.runtime.container.runtime.manager import DependencyManager
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.providers import Provider
from template_app.runtime.container.types import DependencyScope


# -------------------------
# Helpers
# -------------------------

class ServiceA:
    def __init__(self):
        self.value = "A"


class ServiceB:
    def __init__(self, a: ServiceA):
        self.a = a


def make_provider(factory):
    return Provider(factory=factory, scope=DependencyScope.SCOPED)


# -------------------------
# BASIC RESOLUTION
# -------------------------

@pytest.mark.asyncio
async def test_transient_resolution():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    a1 = await manager.resolve(ServiceA)
    a2 = await manager.resolve(ServiceA)

    assert a1 is not a2
    assert a1.value == "A"


# -------------------------
# SINGLETON
# -------------------------

@pytest.mark.asyncio
async def test_singleton_resolution():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    # force singleton scope (adjust if scope enum differs)
    manager._registry.get(ServiceA).provider.scope = manager._registry.get(ServiceA).provider.scope.SINGLETON

    a1 = await manager.resolve(ServiceA)
    a2 = await manager.resolve(ServiceA)

    assert a1 is a2


# -------------------------
# SCOPED
# -------------------------

@pytest.mark.asyncio
async def test_scoped_resolution():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    scope = manager.create_scope()

    a1 = await manager.resolve(ServiceA, scope_id=scope.id)
    a2 = await manager.resolve(ServiceA, scope_id=scope.id)

    assert a1 is a2


# -------------------------
# DIFFERENT SCOPES
# -------------------------

@pytest.mark.asyncio
async def test_scoped_isolation():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    scope1 = manager.create_scope()
    scope2 = manager.create_scope()

    a1 = await manager.resolve(ServiceA, scope_id=scope1.id)
    a2 = await manager.resolve(ServiceA, scope_id=scope2.id)

    assert a1 is not a2


# -------------------------
# DEPENDENCY INJECTION
# -------------------------

@pytest.mark.asyncio
async def test_dependency_injection():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    def factory(m):
        a = m.resolve(ServiceA)
        return ServiceB(a)

    manager.register(
        ServiceB,
        make_provider(factory),
        namespace=Namespace("plugin.test"),
    )

    b = await manager.resolve(ServiceB)

    assert isinstance(b, ServiceB)
    assert isinstance(b.a, ServiceA)


# -------------------------
# VISIBILITY BLOCKING
# -------------------------

@pytest.mark.asyncio
async def test_visibility_block():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.internal"),
    )

    with pytest.raises(Exception):
        await manager.resolve(
            ServiceA,
            requester=Namespace("plugin.external"),
        )


# -------------------------
# CYCLE DETECTION
# -------------------------

@pytest.mark.asyncio
async def test_cycle_detection():
    manager = DependencyManager()

    class A:
        pass

    class B:
        pass

    def factory_a(m):
        return m.resolve(B)

    def factory_b(m):
        return m.resolve(A)

    manager.register(A, make_provider(factory_a), namespace=Namespace("plugin.test"))
    manager.register(B, make_provider(factory_b), namespace=Namespace("plugin.test"))

    with pytest.raises(Exception):
        await manager.resolve(A)


# -------------------------
# SCOPE LIFECYCLE
# -------------------------

def test_scope_lifecycle():
    manager = DependencyManager()

    scope = manager.create_scope()
    assert manager._scopes.exists(scope.id)

    manager.close_scope(scope.id)
    assert not manager._scopes.exists(scope.id)


# -------------------------
# GRAPH SNAPSHOT
# -------------------------

@pytest.mark.asyncio
async def test_snapshot_exists():
    manager = DependencyManager()

    manager.register(
        ServiceA,
        make_provider(lambda m: ServiceA()),
        namespace=Namespace("plugin.test"),
    )

    await manager.resolve(ServiceA)

    snapshot = manager.snapshot()

    assert snapshot.graph is not None
