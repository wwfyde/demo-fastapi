import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from demo_fastapi import crud
from demo_fastapi.core.config import settings
from demo_fastapi.core.db import engine
from demo_fastapi.core.deps import get_db, oauth2_scheme
from demo_fastapi.core.security import get_current_active_user, verify_password
from demo_fastapi.models import User
from demo_fastapi.schemas import UserCreate, UserModel
from demo_fastapi.schemas.token import Token

router = APIRouter()

logger = logging.getLogger(__name__)


def authenticate_user(username: str, password: str) -> UserModel | bool:
    """
    严重用户的账号密码是否正确
    :param username:
    :param password:
    :return:
    """
    with Session(engine) as session:
        stmt = select(User).where(User.username == username)
        user = session.scalars(stmt).one_or_none()
        if not user:
            return False
        # Note: password_hash
        if not verify_password(password, user.hashed_password):
            return False
        user = UserModel.model_validate(user)
        return user


def create_access_token(data: dict, expire_delta: timedelta | None = None):
    to_encode = data.copy()
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/oauth2")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.info("hello")
    return {"token": token}


@router.get("/users/me", response_model=UserModel)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    user = UserModel.model_validate(current_user)
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    获取Token

    :param form_data:
    :return:
    """
    # 用户认证
    logger.info(f"{form_data.username}, {form_data.password}")
    user: UserModel = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.username}, expire_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users/", response_model=UserModel)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = crud.crud_user.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.crud_user.create_user(db=db, user=user)


@router.get("/users/", response_model=list[UserModel])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.crud_user.get_users(db, skip=skip, limit=limit)
    return users


@router.get(
    "/users/{user_id: int}",
    response_model=UserModel,
)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.crud_user.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
