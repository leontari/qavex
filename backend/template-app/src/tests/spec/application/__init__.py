"""
Application builder tests.

Tests for:
    ApplicationBuilder
    KernelLauncher
    installation
    composition
    startup orchestration
    transport lifecycle
    module lifecycle
    plugin lifecycle

Application initialization flow v3:
----------------------------------
bootstrap_kernel()
    ↓
creates kernel only

ApplicationBuilder
    ↓
composes application

KernelLauncher
    ↓
runs application

"""
