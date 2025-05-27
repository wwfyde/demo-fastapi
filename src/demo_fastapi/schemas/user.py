from pydantic import BaseModel, ConfigDict, SecretStr


class UserModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    username: str
    email: str | None = None
    full_name: str | None = None
    is_disabled: bool | None = None
    hashed_password: SecretStr | None = None
    # items: list[item.Item] = []
    is_active: bool | None = None
    id: int | None = None


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    username: str | None = None
    is_superuser: bool


class UserUpsert(UserBase):
    password: str | None = None
    username: str | None = None
    is_superuser: bool | None = None
