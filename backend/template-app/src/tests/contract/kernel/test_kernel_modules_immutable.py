import pytest




def test_kernel_modules_are_immutable() -> None:
    kernel = bootstrap_kernel()

    with pytest.raises(AttributeError):
        kernel.modules.append(object())
