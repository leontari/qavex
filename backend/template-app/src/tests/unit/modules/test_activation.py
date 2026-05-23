from __future__ import annotations

from template_app.runtime.module import (
    ModuleCapability,
    ModuleManifest,
)
from template_app.runtime.module.lifecycle import (
    activate,
)


class FakeModule:
    pass


def test_activate_returns_same_manifests() -> None:
    manifests = (
        ModuleManifest(
            name="fake",
            module=FakeModule(),
            capabilities=frozenset({
                ModuleCapability.ROUTER,
            }),
        ),
    )

    activated = activate(manifests)

    assert activated == manifests
