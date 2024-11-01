from typing import Annotated

from fastapi import APIRouter, Cookie, Depends

from .schemas import CookieSchema

router = APIRouter()


@router.get("/cookies", summary="Cookies, 0.115 特性")
async def read_cookies(cookies: Annotated[CookieSchema, Cookie()]):
    # TODO  Schema 存在问题, 传入时只能传入一个
    return {"cookies": cookies}


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@router.get("/depends/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
