from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int
    msg: str | None = None
    data: dict | list[dict] | None = None
    error: str | None = None
    success: bool = True
