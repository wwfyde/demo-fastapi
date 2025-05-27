import random

from pydantic import BaseModel, ConfigDict, Field


class OrderModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int = Field(default_factory=lambda: random.getrandbits(32), title="ID")
    user_id: int = Field(..., title="用户ID")
    name: str | None = Field(default=None, title="订单名称")

    def create(self, data: dict):
        """
        创建订单
        :param data:
        :return:
        """
        pass

    def update(self, data: dict):
        """
        更新订单
        Args:
            data:

        Returns:
        """


if __name__ == "__main__":
    print(OrderModel(user_id=12))
