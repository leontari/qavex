"""helper presets."""
from template_app.runtime.modules.capabilities import (
    ModuleCapability,
)


FULL_CAPABILITIES = frozenset({
    ModuleCapability.ROUTER,
    ModuleCapability.EVENT_BUS,
    ModuleCapability.INFRASTRUCTURE,
    ModuleCapability.DEPENDENCIES,
})


ROUTER_ONLY = frozenset({
    ModuleCapability.ROUTER,
})
