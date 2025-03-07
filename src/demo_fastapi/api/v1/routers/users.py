import logging
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from passlib.context import CryptContext
from requests import Session
from starlette import status

from demo_fastapi import crud
from demo_fastapi.api.deps import (fake_users_db, get_current_active_user,
                                   get_db, get_user, oauth2_scheme)
from demo_fastapi.core.config import settings
from demo_fastapi.schemas import UserCreate, UserModel
from demo_fastapi.schemas.token import Token

router = APIRouter()

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    # Note: password_hash
    if not verify_password(password, get_password_hash(password)):
        return False
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


@router.get("/oauth2/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    logger.info("hello")
    return {"token": token}


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
):
    return current_user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    # 用户认证
    logger.info(f"{fake_users_db}, {form_data.username}, {form_data.password}")
    user: UserModel = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
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
    #
    # # 从数据库获取用户信息
    # user_dict = fake_users_db.get(form_data.username)
    # if not user_dict:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    # # check password
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    # if not hashed_password:
    #     raise HTTPException(status_code=400, detail="Incorrect username or password")
    #
    # return {"access_token": user.username, "token_type": "bearer"}


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
