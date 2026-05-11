from template_app.models.sqlalchemy_base import Base


def test_metadata_has_tables():
    assert "users" in Base.metadata.tables
