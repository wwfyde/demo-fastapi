from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request

from demo_fastapi.core.config import settings
from demo_fastapi.core.deps import get_current_active_user, verify_header_token, verify_token
from demo_fastapi.core.security import authenticate_user, create_access_token, verify_access_token
from demo_fastapi.models import User
from demo_fastapi.schemas import UserModel
from demo_fastapi.schemas.token import Token

router = APIRouter()


class TokenCreate(BaseModel):
    # username: str
    user_id: int | str = None
    name: str
    # expires_delta: int | None = None
    expires_in: int | None = -1


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """
    获取Token
    """
    # 用户认证
    # logger.info(f"{form_data.username}, {form_data.password}")
    user: UserModel = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(subject=user.username, expires_delta=settings.access_token_expire_days)
    expires_in = datetime.now() + timedelta(days=settings.access_token_expire_days)

    return Token(access_token=access_token, token_type="bearer", expires_in=int(expires_in.timestamp()))


class FormData(BaseModel):
    grant_type: str = "client_credentials"
    client_id: str = "demo"
    client_secret: str = "demo"
    expires_in: int | None = None


@router.post("/generate_access_token", summary="签发Access Token入口, 支持长期有效")
async def generate_access_token(
    token: TokenCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )
    sub = token.user_id
    if token.expires_in <= 0:
        # 永久有效
        expire_delta = timedelta(days=365 * 100)  # 100年
    else:
        expire_delta = timedelta(days=token.expires_in)
    access_token = create_access_token(subject=sub, expires_delta=expire_delta)

    return Token(access_token=access_token, token_type="bearer", expires_in=token.expires_in)


@router.get("/token/verify_token_example", summary="仅需验证token 无需用户")
async def verify_token_example(
    token: Annotated[str, Depends(verify_token)],
):
    """
    测试token验证
    :param token:
    :return:
    """
    return {"message": "Hello, World!", "token": token}


@router.get("/token/api_key_header", summary="自定义Header证")
async def api_key_header(
    request: Request,
    # authorization: Annotated[str, Header(alias="Authorization")] = None,  # not work https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#fixed-fields-10
    # credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    secret_key: Annotated[str, Header(alias="X-Secret-Key")] = None,
    # token: Annotated[str, Depends(verify_token)],
):
    """
    测试token验证
    """
    token = secret_key
    print(request.headers)
    print(token)
    data = verify_access_token(token)
    # verify_token()
    return {"message": "Hello, World!", "token": data}


@router.get("/tokens/credential", summary="自定义Authorization凭证")
async def hello_custom(
    request: Request,
    # authorization: Annotated[str, Header(alias="Authorization")] = None,  # not work https://github.com/OAI/OpenAPI-Specification/blob/main/versions/3.0.2.md#fixed-fields-10
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())],
    # token: Annotated[str, Depends(verify_token)],
):
    """
    测试token验证
    """
    token = credentials.credentials
    print(request.headers)
    print(token)
    data = verify_access_token(token)
    # verify_token()
    return {"message": "Hello, World!", "token": data}


@router.post("/token/verify_api_key_header", summary="验证API Key Header")
async def verify_api_key_header(
    request: Request,
    api_key: Annotated[str, Header(alias="X-Api-Key")] = None,
    header_token: str = Depends(verify_header_token),
):
    # api_key = request.headers.get("X-Api-Key")
    return {"api_key": api_key, "header_token": header_token}
