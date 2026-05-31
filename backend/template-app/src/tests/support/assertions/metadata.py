"""Metadata specific assertions."""
from __future__ import annotations

from template_app.runtime.kernel.runtime.metadata import RuntimeMetadata


def assert_metadata_complete(
    metadata: RuntimeMetadata,
) -> None:
    assert metadata.descriptor is not None
    assert metadata.capabilities is not None
    assert metadata.freeze is not None
