from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    user = User(username='hugo', email='hugo@gmail.com', password='123')
    session.add(user)
    session.commit()
    session.refresh(user)  # atualiza o id e data com o banco

    result = session.scalar(select(User).where(User.email == 'hugo@gmail.com'))

    assert result.username == 'hugo'
    assert user.id == 1
