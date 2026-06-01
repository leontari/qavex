from __future__ import annotations

from pathlib import Path

FORBIDDEN_IMPORTS = (
    "ApplicationBuilder",
    "bootstrap_kernel",
    "TransportFactory",
    "create_http_app",
)

ALLOWED_DIRS = (
    "launcher",
    "runtime/application",
)


def test_composition_objects_not_used_outside_allowed_layers():
    root = Path("template_app")

    violations: list[str] = []

    for py_file in root.rglob("*.py"):

        relative = py_file.relative_to(root)

        path_str = str(relative)

        if any(
            path_str.startswith(prefix)
            for prefix in ALLOWED_DIRS
        ):
            continue

        source = py_file.read_text()

        for forbidden in FORBIDDEN_IMPORTS:
            if forbidden in source:
                violations.append(
                    f"{path_str}: {forbidden}",
                )

    assert not violations, (
        "\n".join(violations)
    )


from __future__ import annotations

from pathlib import Path


FORBIDDEN_IMPORTS = (
    "bootstrap_kernel",
    "ApplicationBuilder",
)


ALLOWED_PATHS = (
    "runtime/application",
    "launcher",
)


def test_composition_objects_are_not_used_outside_composition_layer() -> None:

    root = Path("template_app")

    for file in root.rglob("*.py"):

        path = str(file)

        if any(
            allowed in path
            for allowed in ALLOWED_PATHS
        ):
            continue

        source = file.read_text()

        for forbidden in FORBIDDEN_IMPORTS:
            assert forbidden not in source, (
                f"{forbidden} found in {path}"
            )
