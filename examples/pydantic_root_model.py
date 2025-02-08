from pydantic import BaseModel, RootModel


class MyModel(BaseModel):
    data: RootModel[list[str]]


if __name__ == "__main__":
    model1 = MyModel(data=["1", "2"])
    print(model1)
