import dotenv
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/postgres")
async def postgres():

    return {}


if __name__ == '__main__':
    dotenv.load_dotenv()