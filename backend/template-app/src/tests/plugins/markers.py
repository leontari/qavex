from __future__ import annotations


def pytest_configure(config) -> None:
    """
    Register test markers.
    """

    markers = [
        "unit: fast isolated tests",
        "integration: runtime integration tests"
        "e2e: end-to-end tests",
        "spec: architecture/specification tests",
        "slow: expensive tests"
        "transport",
        "messaging",
        "lifecycle",
        "infrastructure",
        "modules",
        "runtime",
    ]

    for marker in markers:
        config.addinivalue_line("markers", marker)
