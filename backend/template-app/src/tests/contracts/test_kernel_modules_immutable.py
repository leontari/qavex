import pytest

from template_app.bootstrap.runtime.bootstrap import (
    bootstrap_application,
)


def test_kernel_modules_are_immutable() -> None:
    kernel = bootstrap_application()

    with pytest.raises(AttributeError):
        kernel.modules.append(object())
