from booktrack_fastapi.models import User


def test_create_user(session):
    user = User(
        username='test',
        email='test@test',
        password='secret'
    )

    session.add(user)
    session.commit()

    assert user.username == 'test'
