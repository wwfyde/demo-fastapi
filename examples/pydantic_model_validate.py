from pydantic import BaseModel


class MyModel(BaseModel):
    name: str
    id: str
    desc: str


def main():
    sample1 = dict(name="John", id="1", desc="Hello")
    my_model1 = MyModel.model_validate(sample1)
    print(my_model1)


if __name__ == "__main__":
    main()
