from template_app.services.auth_service import AuthService


def test_password_hashing():
    hashed = AuthService.hash_password("secret")
    assert hashed != "secret"
    assert AuthService.verify_password("secret", hashed)
