from template_app.runtime.container.models.keys import DependencyKey
from template_app.runtime.container.models.namespace import Namespace


class Dummy:
    pass


def test_key_identity():
    k1 = DependencyKey(Namespace("a.b"), Dummy)
    k2 = DependencyKey(Namespace("a.b"), Dummy)

    assert k1 == k2


def test_key_node_id():
    key = DependencyKey(Namespace("plugin.auth"), Dummy)

    assert "plugin.auth" in key.node_id
    assert "Dummy" in key.node_id
