"""
Runtime execution pipeline.

Responsible for:
    runtime orchestration
"""

from __future__ import annotations

from template_app.runtime.lifecycle.hooks import LifecycleHook
from template_app.runtime.lifecycle.manager import LifecycleManager
from template_app.runtime.lifecycle.registry import LifecycleRegistry

__all__ = [
    "LifecycleHook",
    "LifecycleManager",
    "LifecycleRegistry",
]
