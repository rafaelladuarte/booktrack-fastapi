from booktrack_fastapi.exameple_models import User
from sqlalchemy import select


def test_create_user(session):
    user = User(username='test', email='test@test', password='secret')

    session.add(user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'test'))

    assert user.username == 'test'
