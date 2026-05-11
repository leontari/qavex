from template_app.models.user import User


def test_user_model_from_orm():
    orm = type(
        "Obj",
        (),
        {"id": 1, "email": "x@y.com", "full_name": None, "is_active": True},
    )
    user = User.model_validate(orm)

    assert user.id == 1
    assert user.email == "x@y.com"
