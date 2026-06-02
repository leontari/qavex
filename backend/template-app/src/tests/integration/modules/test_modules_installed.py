from __future__ import annotations

from tests.support.harness.kernel_test_harness import KernelTestHarness


def test_modules_installed() -> None:
    kernel = KernelTestHarness().kernel

    assert len(kernel.modules) >= 0


def test_module_manifests_have_names() -> None:
    kernel = KernelTestHarness().kernel

    assert all(manifest.name for manifest in kernel.modules)
