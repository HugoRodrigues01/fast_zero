from datetime import datetime, timedelta, timezone
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import decode, encode
from jwt.exceptions import PyJWTError
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from fast_zero.database import get_session
from fast_zero.models import User
from fast_zero.settings import Settings

pwd_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str):
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data_clain: dict):
    to_encode = data_clain.copy()

    expire = datetime.now(tz=timezone.utc) + timedelta(
        minutes=Settings().EXCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    encoded_jwt = encode(to_encode, Settings().SECRET_KEY, algorithm=Settings().ALGORITHM)
    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_scheme),
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        payload = decode(token, Settings().SECRET_KEY, algorithms=[Settings().ALGORITHM])
        username = payload.get('sub')

        if not username:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_db = session.scalar(select(User).where(User.email == username))

    if not user_db:
        raise credentials_exception
    return user_db
