from __future__ import annotations

from template_app.runtime.kernel.kernel import RuntimeKernel
from template_app.runtime.modules import ModuleManifest


def test_kernel_exposes_module_manifest_snapshot(kernel: RuntimeKernel) -> None:
    """
    Kernel should expose installed modules as immutable manifest snapshot.
    """
    assert isinstance(kernel.modules, tuple)


def test_kernel_modules_are_manifests(kernel: RuntimeKernel) -> None:
    """
    Kernel should expose only ModuleManifest objects.
    """
    assert all(
        isinstance(module, ModuleManifest)
        for module in kernel.modules
    )


def test_kernel_modules_boundary_is_read_only(kernel: RuntimeKernel) -> None:
    """
    Kernel module exposure should remain immutable.
    """
    modules = kernel.modules

    assert not hasattr(modules, "append")


def test_kernel_module_boundary_is_runtime_owned(kernel: RuntimeKernel) -> None:
    """
    Kernel module manifests should originate
    from runtime-owned module registry.
    """
    assert tuple(kernel.runtime.modules.registry.modules) == kernel.modules
