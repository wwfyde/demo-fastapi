import os

# import requests
from dotenv import dotenv_values, find_dotenv, load_dotenv

if __name__ == "__main__":
    # requests.get(url="https://www.google.com")
    # print(__package__)
    # print(sys.path)
    # # Not Recommended use finde_dotenv instead
    # env_path = Path('.').absolute().parent.joinpath('.env')
    # load_dotenv(env_path)
    # with open(env_path) as f:
    #     for line in f:
    #         print(line.strip(), end='')
    # print(env_path)
    env_file = find_dotenv(filename=".env.local")
    print(env_file)
    env_files = [".env", ".env.local", ".env.prod"]
    d = {}
    for env_file in env_files:
        load_dotenv(find_dotenv(filename=env_file), override=True)
        envs = dotenv_values(
            find_dotenv(env_file),
        )
        d.update(dotenv_values(env_file))
    print(d)
    print(os.environ)
    config = {
        **dotenv_values(find_dotenv(filename=".env")),
        **dotenv_values(find_dotenv(filename=".env.local")),
        **dotenv_values(find_dotenv(filename=".env.prod")),
    }
    print(f"{config=}")

    load_dotenv(find_dotenv(filename=".env.local"))
    print(dotenv_values(env_file))
    print(os.environ)
    print(os.getenv("PGUSER"), os.getenv("PGPASS"))
