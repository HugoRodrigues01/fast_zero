from http import HTTPStatus


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    # client = TestClient(app)   avarrange (organização)

    response = client.get('/')  # act (execução)

    assert response.status_code == HTTPStatus.OK  # assert
    assert response.json() == {'message': 'Hello World!!'}
