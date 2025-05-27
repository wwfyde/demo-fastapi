from pydantic import BaseModel, Field


class Product(BaseModel):
    id: int = Field()
    name: str = Field()
    category: str = Field()
    price: float = Field()
    tags: list[str] = Field()
    in_stock: bool = Field()
    has_image: bool = Field()
    has_sku: bool = Field()

    def create(self, data: dict):
        pass

    def update(self, data: dict):
        pass

    def upsert(self, data: dict):
        pass

    def delete(self, id: int):
        pass
