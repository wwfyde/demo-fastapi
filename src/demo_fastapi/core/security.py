from datetime import datetime, timedelta, timezone
from typing import Any, Union

import bcrypt
from fastapi import HTTPException
from jose import JWTError, jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from demo_fastapi.core.config import settings
from demo_fastapi.core.db import async_engine
from demo_fastapi.models import User
from demo_fastapi.schemas import UserModel


def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    """
    Args:
        subject:
        expires_delta: 过期时间间隔

    Returns: JWT

    """
    if expires_delta is None:
        expires_delta = timedelta(days=settings.access_token_expire_days)
    current_time = datetime.now(tz=timezone.utc)
    expiration_time = current_time + expires_delta
    to_encode = {"exp": expiration_time, "sub": str(subject), "iat": current_time}
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt


def verify_access_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
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
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))


def get_password_hash(password: str) -> str:
    # 移除 passlib依赖
    hashed = bcrypt.hashpw(
        # password.encode("utf-8"), settings.secret_key.encode("utf-8")
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )
    return hashed.decode("utf-8")


async def authenticate_user(username: str, password: str) -> UserModel | None:
    """
    验证用户的账号密码是否正确
    """
    async with AsyncSession(async_engine) as session:
        stmt = select(User).where(User.username == username)
        user = (await session.scalars(stmt)).one_or_none()
        if not user:
            return None
        # Note: password_hash
        if not verify_password(password, user.hashed_password):
            return None
        user = UserModel.model_validate(user)
        return user


if __name__ == "__main__":
    print(verify_password("123456", get_password_hash("123456")))
    token = create_access_token("wwfyde")
    print(verify_access_token(token))
