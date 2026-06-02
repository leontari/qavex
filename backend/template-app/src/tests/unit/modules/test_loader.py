# from __future__ import annotations
#
# from tests.support.factories.module_context import (
#     build_module_context,
# )
# from tests.support.factories.modules import (
#     build_fake_module,
# )
#
#
# def test_loader_executes_module_setup() -> None:
#
#     module = build_fake_module()
#
#     context = build_module_context()
#
#     module.setup(context)
#
#     startup_hooks = (
#         context.runtime
#         .lifecycle_registry
#         .startup_hooks
#     )
#
#     assert startup_hooks
