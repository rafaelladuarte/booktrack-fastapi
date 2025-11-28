from http import HTTPStatus

from jwt import decode

from booktrack_fastapi.core.security import (
    SECRET_KEY,
    create_access_token,
)


def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert 'exp' in decoded
    assert decoded['type'] == 'access'

