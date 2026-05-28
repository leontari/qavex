"""fakes injection."""

from tests.support.fakes.cache import FakeCacheProvider
from tests.support.fakes.database import FakeDatabaseProvider
from tests.support.fakes.queue import FakeQueueProvider

from template_app.runtime.infrastructure.registry import (
    InfrastructureRegistry,
)

from template_app.runtime.infrastructure.runtime import (
    InfrastructureRuntime,
)


def apply_fake_infrastructure(kernel) -> None:

    registry = InfrastructureRegistry(
        cache=FakeCacheProvider(),
        database=FakeDatabaseProvider(),
        queue=FakeQueueProvider(),
    )

    kernel.runtime.infrastructure = InfrastructureRuntime(
        registry=registry,
    )
