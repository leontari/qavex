from __future__ import annotations

import ast
import inspect

import template_app.main


def _get_source_tree():
    return ast.parse(inspect.getsource(template_app.main))


def test_main_does_not_use_builder() -> None:
    tree = _get_source_tree()

    assert not any(
        isinstance(node, ast.Name) and node.id == "ApplicationBuilder"
        for node in ast.walk(tree)
    )


def test_main_does_not_use_bootstrap_kernel() -> None:
    tree = _get_source_tree()

    assert not any(
        isinstance(node, ast.Name) and node.id == "bootstrap_kernel"
        for node in ast.walk(tree)
    )
