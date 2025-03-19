from datetime import datetime, timedelta, timezone
from typing import Annotated, Any, Union

import bcrypt
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from demo_fastapi.core.config import settings
from demo_fastapi.core.deps import get_db, oauth2_scheme
from demo_fastapi.models import User


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def verify_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # result = jwt.decode(hashed_password, settings.secret_key, algorithms=[ALGORITHM])
    # print(result)
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def get_password_hash(password: str) -> str:
    hashed = bcrypt.hashpw(
        # password.encode("utf-8"), settings.secret_key.encode("utf-8")
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_db)
) -> User:
    """
    获取当前用户
    :param session:
    :param token:
    :return:
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.jwt_algorithm]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    with session:
        stmt = select(User).where(User.username == username)
        result = session.execute(stmt)
        user = result.scalars().one_or_none()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


if __name__ == "__main__":
    print(verify_password("123456", get_password_hash("123456")))
    token = create_access_token("wwfyde")
    print(verify_access_token(token))
