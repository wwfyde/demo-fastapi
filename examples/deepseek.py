# Please install OpenAI SDK first: `pip3 install openai`
import os

from openai import OpenAI


def main():
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

    if DEEPSEEK_API_KEY == "":
        print("Please set DEEPSEEK_API_KEY first.")
        return
    client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
    content = input("请输入问题：")

    response = client.chat.completions.create(
        # model="deepseek-chat",
        model="deepseek-reasoner",
        messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {
                "role": "user",
                # "content": "牛肉焯水的原理与科学依据, 作用与目的, 与技巧, 尤其是保持肉嫩. 去除血水与腥味",
                "content": content,
            },
        ],
        stream=False,
    )

    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
