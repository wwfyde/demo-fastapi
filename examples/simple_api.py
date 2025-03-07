from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{prompt}")
async def read_item(prompt: str):
    url = "https://open-1317903499.cos.ap-guangzhou.myqcloud.com/docker-compose.yml"
    return {"prompt": prompt, "url": url}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
