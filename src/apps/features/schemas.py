from pydantic import BaseModel


class CookieSchema(BaseModel):
    name: str | None = None
    value: str | None = None
    domain: str | None = None