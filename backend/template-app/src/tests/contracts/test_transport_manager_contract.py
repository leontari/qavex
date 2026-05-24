from template_app.transports.manager import TransportManager


def test_transport_manager_hides_internal_list() -> None:
    manager = TransportManager()

    assert not hasattr(manager, "transports_list")
