from http import HTTPStatus

from jwt import decode

from fast_zero.security import create_access_token
from fast_zero.settings import Settings


def test_jwt():
    data = {'sub': 'test@gmail.com'}
    token = create_access_token(data)

    result = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])

    assert result['sub'] == data['sub']
    assert result['exp']


def test_jwt_invalid_token(client):
    response = client.delete('users/1', headers={'Authorization': 'Bearer token-invalid'})

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}
