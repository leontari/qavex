from __future__ import annotations

from template_app.runtime.modules import (
    ModuleManifest,
)

from tests.support.harness.kernel_test_harness import (
    KernelTestHarness,
)


def test_kernel_exposes_module_manifest_snapshot(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose installed modules
    as immutable manifest snapshot.
    """
    modules = kernel_harness.kernel.modules

    assert isinstance(modules, tuple)


def test_kernel_modules_are_manifests(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel should expose only ModuleManifest objects.
    """
    assert all(
        isinstance(module, ModuleManifest)
        for module in kernel_harness.kernel.modules
    )


def test_kernel_modules_boundary_is_read_only(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel module exposure should remain immutable.
    """
    modules = kernel_harness.kernel.modules

    assert not hasattr(modules, "append")


def test_kernel_module_boundary_is_runtime_owned(
    kernel_harness: KernelTestHarness,
) -> None:
    """
    Kernel module manifests should originate
    from runtime-owned module registry.
    """
    assert (
        kernel_harness.kernel.modules
        is kernel_harness.kernel.runtime.modules.registry.modules
    )
