from template_app.bootstrap.modules import (
    ModuleSetupContext,
    ModuleManifest,
    load_modules,
    ModuleCapability,
)
from template_app.bootstrap.modules.apis import (
    ModuleRuntimeAPI,
    ModuleInfraAPI,
    ModuleMessagingAPI,
)
from template_app.bootstrap.runtime.state import RuntimeState
from template_app.bootstrap.lifecycle import (
    LifecycleRegistry,
    LifecycleManager,
)
from template_app.bootstrap.kernel import Container
from template_app.bootstrap.messaging.runtime import (
    RuntimeEventBus,
    RuntimeCommandBus,
    RuntimeQueryBus,
    RuntimeHandlerRegistry,
)


class FakeModule:
    loaded: bool = False

    def setup(self, context: ModuleSetupContext) -> None:
        self.loaded = True


def build_module_context():
    container = Container()
    lifecycle_registry = LifecycleRegistry()
    lifecycle_manager = LifecycleManager(registry=lifecycle_registry)

    messaging_registry = RuntimeHandlerRegistry()

    runtime = RuntimeState(
        container=container,
        lifecycle_registry=lifecycle_registry,
        lifecycle_manager=lifecycle_manager,
        infrastructure_registry=None,  # ok for fake tests if allowed
        messaging_registry=messaging_registry,
        event_bus=RuntimeEventBus(registry=messaging_registry),
        command_bus=RuntimeCommandBus(registry=messaging_registry),
        query_bus=RuntimeQueryBus(registry=messaging_registry),
    )

    return ModuleSetupContext(
        runtime=ModuleRuntimeAPI(
            app=None,
            container=container,
            lifecycle_registry=lifecycle_registry,
        ),
        infra=ModuleInfraAPI(registry=None),
        messaging=ModuleMessagingAPI(
            event_bus=RuntimeEventBus(messaging_registry),
            command_bus=RuntimeCommandBus(messaging_registry),
            query_bus=RuntimeQueryBus(messaging_registry),
        ),
        capabilities=frozenset({ModuleCapability.ROUTER}),
    )


def test_loader_executes_module_setup() -> None:

    module = FakeModule()

    manifests = (
        ModuleManifest(
            name="fake",
            module=module,
            capabilities=frozenset({ModuleCapability.ROUTER}),
        ),
    )

    context = build_module_context()

    load_modules(
        manifests=manifests,
        context=context,
    )

    assert module.loaded is True
