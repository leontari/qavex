"""Tests for DependencyGraph."""

from types import MappingProxyType

from template_app.runtime.container.models.dependency import (
    DependencyID,
)
from template_app.runtime.container.models.namespace import Namespace
from template_app.runtime.container.runtime.graph import (
    DependencyGraph,
)


class ServiceA: ...


class ServiceB: ...


class ServiceC: ...


def make_dependency(
    contract: type,
    namespace: str = "test",
) -> DependencyID:
    return DependencyID(
        namespace=Namespace(namespace),
        contract=contract,
    )


def test_add_node() -> None:
    graph = DependencyGraph()

    dependency = make_dependency(ServiceA)

    graph.add_node(dependency)

    assert graph.has_node(dependency)
    assert graph.node_count == 1
    assert graph.edge_count == 0


def test_add_edge_registers_nodes() -> None:
    graph = DependencyGraph()

    source = make_dependency(ServiceA)
    target = make_dependency(ServiceB)

    graph.add_edge(source, target)

    assert graph.has_node(source)
    assert graph.has_node(target)

    assert graph.node_count == 2
    assert graph.edge_count == 1


def test_add_duplicate_edge_is_ignored() -> None:
    graph = DependencyGraph()

    source = make_dependency(ServiceA)
    target = make_dependency(ServiceB)

    graph.add_edge(source, target)
    graph.add_edge(source, target)
    graph.add_edge(source, target)

    assert graph.edge_count == 1


def test_successors_returns_direct_dependencies() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)
    c = make_dependency(ServiceC)

    graph.add_edge(a, b)
    graph.add_edge(a, c)

    assert graph.successors(a) == frozenset({b, c})


def test_successors_returns_empty_set_for_unknown_node() -> None:
    graph = DependencyGraph()

    dependency = make_dependency(ServiceA)

    assert graph.successors(dependency) == frozenset()


def test_predecessors_returns_direct_dependents() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)
    c = make_dependency(ServiceC)

    graph.add_edge(a, c)
    graph.add_edge(b, c)

    assert graph.predecessors(c) == frozenset({a, b})


def test_predecessors_returns_empty_set_for_unknown_node() -> None:
    graph = DependencyGraph()

    dependency = make_dependency(ServiceA)

    assert graph.predecessors(dependency) == frozenset()


def test_contains_returns_false_for_unknown_node() -> None:
    graph = DependencyGraph()

    dependency = make_dependency(ServiceA)

    assert not graph.has_node(dependency)


def test_clear_removes_all_nodes_and_edges() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)

    graph.add_edge(a, b)

    graph.clear()

    assert graph.node_count == 0
    assert graph.edge_count == 0
    assert not graph.has_node(a)
    assert not graph.has_node(b)


def test_nodes_returns_immutable_view() -> None:
    graph = DependencyGraph()

    dependency = make_dependency(ServiceA)

    graph.add_node(dependency)

    nodes = graph.nodes

    assert isinstance(nodes, frozenset)

    try:
        nodes.add(dependency)
    except AttributeError:
        pass
    else:
        raise AssertionError("nodes must be immutable")


def test_edges_returns_read_only_mapping() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)

    graph.add_edge(a, b)

    edges = graph.edges

    assert isinstance(edges, MappingProxyType)

    try:
        edges[a] = frozenset()
    except TypeError:
        pass
    else:
        raise AssertionError("edges must be immutable")


def test_reverse_edges_returns_read_only_mapping() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)

    graph.add_edge(a, b)

    reverse_edges = graph.reverse_edges

    assert isinstance(reverse_edges, MappingProxyType)

    try:
        reverse_edges[b] = frozenset()
    except TypeError:
        pass
    else:
        raise AssertionError("reverse_edges must be immutable")


def test_edge_count_with_multiple_edges() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)
    c = make_dependency(ServiceC)

    graph.add_edge(a, b)
    graph.add_edge(a, c)
    graph.add_edge(b, c)

    assert graph.edge_count == 3


def test_predecessors_and_successors_are_consistent() -> None:
    graph = DependencyGraph()

    a = make_dependency(ServiceA)
    b = make_dependency(ServiceB)

    graph.add_edge(a, b)

    assert b in graph.successors(a)
    assert a in graph.predecessors(b)


def test_large_graph() -> None:
    graph = DependencyGraph()

    previous = None

    for index in range(1000):

        contract = type(f"Service{index}", (), {})

        current = make_dependency(contract)

        if previous:
            graph.add_edge(previous, current)

        previous = current

    assert graph.node_count == 1000
    assert graph.edge_count == 999
