import pytest

from runtime.container.manager import DependencyManager
from runtime.container.namespace import Namespace
from runtime.container.providers import SingletonProvider
from runtime.container.types import DependencyVisibility
from runtime.container.exceptions import (
    DependencyVisibilityError,
)


class Service:
    pass


def test_private_visibility() -> None:
    manager = DependencyManager()

    manager.register(
        Service,
        SingletonProvider(lambda _: Service()),
        namespace=Namespace("plugin.auth"),
        visibility=DependencyVisibility.PRIVATE,
    )

    with pytest.raises(DependencyVisibilityError):
        manager.resolve(
            Service,
            requester=Namespace("plugin.billing"),
        )
