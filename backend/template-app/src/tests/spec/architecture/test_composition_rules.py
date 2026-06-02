# from __future__ import annotations
#
# import ast
# from pathlib import Path
#
# ROOT = Path("template_app")
#
# FORBIDDEN_IMPORTS = {
#     "template_app.runtime.application.builder.ApplicationBuilder",
#     "template_app.runtime.kernel.bootstrap.bootstrap_kernel",
#     "template_app.runtime.transports.factory.TransportFactory",
#     "template_app.runtime.transports.http.factory.create_http_app",
# }
#
#
# def extract_imports(file: Path) -> set[str]:
#     """Extract real imports using AST (no false positives)."""
#
#     tree = ast.parse(file.read_text(encoding="utf-8"))
#
#     imports: set[str] = set()
#
#     for node in ast.walk(tree):
#         # import x.y.z
#         if isinstance(node, ast.Import):
#             for alias in node.names:
#                 imports.add(alias.name)
#
#         # from x.y import z
#         elif isinstance(node, ast.ImportFrom) and node.module:
#             imports.add(node.module)
#
#     return imports
#
#
# def test_composition_objects_not_used_outside_allowed_layers_ast() -> None:
#     """
#     Enforces architectural boundaries via real import graph.
#
#     No false positives from:
#         - docstrings
#         - comments
#         - logs
#         - string literals
#     """
#
#     violations: list[str] = []
#
#     for file in ROOT.rglob("*.py"):
#         imports = extract_imports(file)
#
#         for forbidden in FORBIDDEN_IMPORTS:
#             module_path = ".".join(forbidden.split(".")[:-1])
#
#             if module_path in imports or forbidden in imports:
#                 violations.append(f"{file}: {forbidden}")
#
#     assert not violations, "\n".join(violations)
