from app.core.utils import normalize_name

def test_normalize_name():
    assert normalize_name(" Alice ") == "alice"
