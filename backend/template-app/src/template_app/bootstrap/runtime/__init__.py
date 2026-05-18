"""
Application kernel constructor.

Actual place where:
- application kernel bootstrapping happens
- transport and runtime adapters are injected into kernel.
"""

from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

__all__ = [
    "bootstrap_application",
]
