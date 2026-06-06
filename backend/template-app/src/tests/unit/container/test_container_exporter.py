from template_app.runtime.container.exporters import (
    export_json,
)

from template_app.runtime.container.exporters import (
    export_dump,
)

from template_app.runtime.container.exporters import (
    export_graph,
)


def test_json_export_contains_contract():
    snapshot = manager.snapshot()

    payload = export_json(snapshot)

    assert "Database" in payload





def test_dump_export_contains_namespace():
    dump = export_dump(
        manager.snapshot(),
    )

    assert "kernel" in dump



def test_graph_export_is_dot():
    graph = export_graph(
        manager.snapshot(),
    )

    assert graph.startswith(
        "digraph Container"
    )
