from runtime.container.graph import DependencyGraph
from runtime.container.exceptions import DependencyCycleError


def test_cycle_detection() -> None:
    graph = DependencyGraph()

    graph.add_edge("A", "B")
    graph.add_edge("B", "C")
    graph.add_edge("C", "A")

    try:
        graph.validate()
    except DependencyCycleError:
        return

    assert False
