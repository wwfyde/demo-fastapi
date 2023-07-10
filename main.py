import sys

import dotenv
from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(debug=True, title='FastAPI演示程序', version='0.1.0')

print(f"sys.path: { sys.path }")

@app.get("/")
async def root():
    print(settings)
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/postgres")
async def postgres():

    return {}


if __name__ == '__main__':
    dotenv.load_dotenv()