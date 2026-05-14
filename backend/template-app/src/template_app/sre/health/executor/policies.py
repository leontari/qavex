"""
Execution policies for the dependency graph health executor.

This module defines rules that control how the dependency-aware health
execution engine behaves under failure conditions, partial outages,
and degraded infrastructure states.

These policies determine:

- whether dependent checks are skipped
- how failures propagate through the graph
- how degraded states are assigned
- retry and fallback behavior
- safe execution boundaries for Kubernetes probes
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class FailureMode(StrEnum):
    """
    Defines how dependency failures are handled.
    """

    STRICT = "strict"
    """
    If a dependency fails, all downstream nodes are skipped.
    """

    SOFT = "soft"
    """
    Downstream nodes still execute but are marked degraded.
    """

    IGNORE = "ignore"
    """
    Dependencies do not affect execution flow.
    """


class DegradedPropagationMode(StrEnum):
    """
    Defines how degraded states propagate in the dependency graph.
    """

    NONE = "none"
    """
    Do not propagate degraded states.
    """

    DOWNSTREAM = "downstream"
    """
    Propagate degraded state to dependent nodes only.
    """

    TRANSITIVE = "transitive"
    """
    Propagate degraded state recursively through all downstream nodes.
    """


@dataclass(slots=True)
class GraphExecutionPolicy:
    """
    Runtime execution policy for dependency graph health checks.

    This policy controls the behavior of the graph executor when handling:

    - failed nodes
    - degraded dependencies
    - partial outages
    - cascading failures
    """

    failure_mode: FailureMode = FailureMode.STRICT

    degraded_mode: DegradedPropagationMode = DegradedPropagationMode.DOWNSTREAM

    skip_on_unhealthy_dependency: bool = True

    allow_partial_results: bool = True

    fail_fast: bool = False

    max_depth: int | None = None
    """
    Optional maximum traversal depth in dependency graph.
    Useful for preventing runaway or misconfigured graphs.
    """

    include_skipped_in_results: bool = True
