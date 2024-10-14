from pydantic import AliasChoices, BaseModel, Field


class Validator(BaseModel):
    page_size: int = Field(default=10, title="每页数量", description="每页数量", deprecated=False,
                           validation_alias=AliasChoices('page_size', 'pageSize', 'PageSize'))


class StudentCreate(BaseModel):
    name: str = Field(default=None, title="学生姓名", description="学生姓名", deprecated=False,
                      validation_alias=AliasChoices('name', 'Name', 'NAME'))
    age: int = Field(default=None, title="学生年龄", description="学生年龄", deprecated=False,
                     validation_alias=AliasChoices('age', 'Age', 'AGE'))
