from fastapi import FastAPI

from demo_fastapi.apps.features import router

app = FastAPI()

app.include_router(router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=5001)
