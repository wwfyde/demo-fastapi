from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


# 待办事项基础模式
class TodoBase(BaseModel):
    title: str
    completed: Optional[bool] = False


# 创建待办事项请求模式
class TodoCreate(TodoBase):
    pass


# 更新待办事项请求模式
class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


# 待办事项数据库模式
class TodoInDB(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime
    title: str

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_name=True,
        alias_generator=to_camel,
    )


# 待办事项返回模式
class TodoResponse(TodoInDB):
    pass
