from fastapi import FastAPI

from template_app.bootstrap.kernel import (
    Container,
)
from template_app.bootstrap.lifecycle import (
    LifecycleRegistry,
)
from template_app.bootstrap.modules.apis import (
    ModuleRuntimeAPI,
)


def build_runtime_api() -> ModuleRuntimeAPI:

    return ModuleRuntimeAPI(
        app=FastAPI(),
        container=Container(),
        lifecycle_registry=LifecycleRegistry(),
    )
