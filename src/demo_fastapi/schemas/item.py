from pydantic import BaseModel, ConfigDict, JsonValue


class ItemBase(BaseModel, from_attributes=True):
    """
    通用模型, ItemBase, UserBase
    """

    title: str
    description: str | None = None
    config: JsonValue
    model_config = ConfigDict(from_attributes=True)


class ItemModel(BaseModel, from_attributes=True):
    """
    ORM parse of Item, or naming with **ItemSchema**, **ItemValidator**
    """

    id: int
    title: str
    description: str
    description2: str
    config: JsonValue
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ItemInDB(ItemBase):
    """
    对象在数据库中的表示, 通常包含敏感数据, 不应该将密码登数据暴露给用户
    """

    id: int
    owner_id: int
    pass


class Item(ItemBase):
    """
    不推荐 ,可能和models 重名, 混淆
    """

    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)


class ItemCreate(ItemBase):
    """
    创建时 ItemSchema, ItemValidater, CreateItemValidator
    """

    alias: str | None = None
    pass


class ItemDelete(BaseModel):
    """
    删除时
    Go 中 Delete<ModelName>Validator, Delete<ModelName>Input
    """

    id: int
    pass


class ItemUpdate(ItemBase):
    """
    更新时, Update<ModelName>Validator, UpdateUserValidator
    Go 中 Update<ModelName>Input
    """

    id: int
    pass


class ItemOut(ItemBase):
    """
    输出时 ItemOut, `ItemResponse`, `ItemResult`, ~~ItemRead~~
    """

    id: int
    pass
