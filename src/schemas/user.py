from pydantic import BaseModel, ConfigDict

from src.schemas import item


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    hashed_password: str | None = None
    items: list[item.Item] = []
    is_active: bool | None = None
    id: int | None = None


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
