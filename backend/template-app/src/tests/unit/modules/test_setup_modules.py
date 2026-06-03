# from template_app.runtime.modules.setup import (
#     setup_modules,
# )
# from template_app.runtime.modules.registry import (
#     ModuleRegistry,
# )
# from tests.support.factories.kernel import (
#     build_testing_kernel,
# )
#
#
# def test_setup_modules_installs_modules() -> None:
#     kernel = build_testing_kernel()
#
#     registry = ModuleRegistry()
#
#     installed = setup_modules(
#         kernel=kernel,
#         registry=registry,
#     )
#
#     assert isinstance(installed, tuple)
