from __future__ import annotations

from template_app.runtime.infrastructure.factories import bootstrap_infrastructure


def test_providers_registered() -> None:
    registry = bootstrap_infrastructure()

    names = {provider.name for provider in registry.providers}

    assert "database" in names
    assert "cache" in names
    assert "queue" in names
