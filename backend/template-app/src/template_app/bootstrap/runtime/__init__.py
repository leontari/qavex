"""
Application kernel constructor.

It's an actual place where:
- application kernel bootstrapping happens
"""

from __future__ import annotations

from template_app.bootstrap.runtime.bootstrap import bootstrap_application

__all__ = [
    "bootstrap_application",
]
