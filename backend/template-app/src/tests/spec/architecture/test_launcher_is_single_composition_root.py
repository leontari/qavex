from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path("template_app")


def find_transport_factory_usage(file: Path) -> bool:
    """Detect real TransportFactory usage via AST imports."""
    tree = ast.parse(file.read_text(encoding="utf-8"))

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and "transport.factory" in node.module:
                return True

        if isinstance(node, ast.Import):
            for alias in node.names:
                if "TransportFactory" in alias.name:
                    return True

    return False


def test_only_launcher_uses_transport_factory() -> None:
    """
    Ensures TransportFactory is only used inside launcher layer.
    """

    offenders: list[str] = []

    for file in ROOT.rglob("*.py"):
        if "launcher" in str(file):
            continue

        try:
            if find_transport_factory_usage(file):
                offenders.append(str(file))
        except SyntaxError:
            # skip invalid files in test context
            continue

    assert not offenders, "\n".join(offenders)
