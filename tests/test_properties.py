from sqlalchemy import select

from booktrack_fastapi.models.properties import Publishers


def test_create_publishers(session):
    pub = Publishers(nome='Aleph')

    session.add(pub)
    session.commit()

    pub = session.scalar(select(Publishers).where(Publishers.nome == 'Aleph'))

    assert pub.nome == 'Aleph'
