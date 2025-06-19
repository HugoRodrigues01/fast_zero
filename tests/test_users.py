from http import HTTPStatus

from fast_zero.schemas import UserPublic


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'usertest',
            'email': 'emailteste@exemple.com',
            'password': 'password',
        },
    )

    # Verificando se foi criado
    assert response.status_code == HTTPStatus.CREATED
    # Verificando o schema userpublic
    assert response.json() == {
        'username': 'usertest',
        'email': 'emailteste@exemple.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'userteste02',
            'password': '123',
            'email': 'emailteste02@exemplo.com',
            'id': user.id,
        },
    )

    assert response.json() == {
        'username': 'userteste02',
        'email': 'emailteste02@exemplo.com',
        'id': user.id,
    }


def test_update_user_with_wrong_user(client, token, other_user):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'userteste02',
            'password': '123',
            'email': 'emailteste02@exemplo.com',
            'id': other_user.id,
        },
    )

    assert response.json() == {'detail': 'not enough permission'}


def test_update_user_not_found_error(client, user, token):
    response = client.put(
        '/users/404',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'userteste02',
            'password': '123',
            'email': 'emailteste02@exemplo.com',
            'id': 404,
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'message': 'user was deleted'}


def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user_not_found_error(client, token):
    response = client.delete('/users/404', headers={'Authorization': f'Bearer {token}'})

    assert response.json() == {'detail': 'Not enough permission'}


def test_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': user.username,
            'email': 'teste02@gmail.com',
            'password': 'nopassword',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'pablo',
            'email': user.email,
            'password': 'nopassword',
        },
    )

    assert response.status_code == HTTPStatus.FORBIDDEN


def test_incorrect_email_or_password(client, user):
    response = client.post(
        'auth/token', data={'username': user.email, 'password': 'password_error'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
