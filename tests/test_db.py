from booktrack_fastapi.models import User


def test_create_user():
    user = User(
        username='test',
        email='test@test',
        password='secret'
    )

    assert user.username == 'test'