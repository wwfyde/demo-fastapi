import asyncio
import os

from dotenv import find_dotenv, load_dotenv
from openai import AsyncOpenAI
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(find_dotenv())


class LLM(BaseModel):
    name: str
    value: str


class Settings(BaseSettings):
    ark_models: list[LLM] = os.getenv(
        "ARK_MODELS",
    )
    ark_api_key: str | None = os.getenv("ARK_API_KEY")
    ark_base_url: str | None = os.getenv("ARK_BASE_URL")

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()


async def main():
    client = AsyncOpenAI(
        api_key=settings.ark_api_key,
        base_url=settings.ark_base_url,
    )
    model = next(
        (model.value for model in settings.ark_models if model.name == "deepseek-v3"),
        None,
    )
    print(model)

    stream = await client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": " this is test",
            }
        ],
        stream=True,
    )
    async for chunk in stream:
        print(chunk.choices[0].delta.content or "", end="")


if __name__ == "__main__":
    print(settings)

    asyncio.run(main())
