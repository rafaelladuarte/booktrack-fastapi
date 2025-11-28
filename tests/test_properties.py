from sqlalchemy import select

from booktrack_fastapi.models.publishers import Publishers


def test_create_publishers(session):
    pub = Publishers(name='Aleph')

    session.add(pub)
    session.commit()

    pub = session.scalar(select(Publishers).where(Publishers.name == 'Aleph'))

    assert pub.name == 'Aleph'
