from __future__ import annotations


def pytest_configure(config) -> None:

    config.addinivalue_line(
        "markers",
        "unit: fast isolated tests",
    )

    config.addinivalue_line(
        "markers",
        "integration: runtime integration tests",
    )

    config.addinivalue_line(
        "markers",
        "e2e: end-to-end tests",
    )

    config.addinivalue_line(
        "markers",
        "spec: architecture/specification tests",
    )

    config.addinivalue_line(
        "markers",
        "slow: expensive tests",
    )
