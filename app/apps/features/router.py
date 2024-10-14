from typing import Annotated

from fastapi import APIRouter, Cookie

from .schemas import CookieSchema

router = APIRouter()


@router.get("/cookies", summary="Cookies, 0.115 特性")
async def read_cookies(cookies: Annotated[CookieSchema, Cookie()]):
    # TODO  Schema 存在问题, 传入时只能传入一个
    return {"cookies": cookies}
