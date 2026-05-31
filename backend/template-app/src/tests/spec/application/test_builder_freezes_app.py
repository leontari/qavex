from __future__ import annotations

from template_app.runtime.application.builder import ApplicationBuilder
from template_app.runtime.kernel.kernel import RuntimeKernel


# def test_builder_freezes_kernel(kernel: RuntimeKernel) -> None:
#     builder = ApplicationBuilder()
#     app = builder.create()
#
#     assert app.kernel.metadata.freeze.frozen is True
#     assert kernel.is_frozen is True
