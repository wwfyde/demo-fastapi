import os
import sys
from pathlib import Path

# import requests
from dotenv import load_dotenv


import dotenv

if __name__ == '__main__':
    # requests.get(url="https://www.google.com")
    print(__package__)
    print(sys.path)
    env_path = Path('.').absolute().parent.joinpath('.env')
    load_dotenv(env_path)
    # with open(env_path) as f:
    #     for line in f:
    #         print(line.strip(), end='')
    # print(env_path)
    print(os.getenv('PGUSER'), os.getenv("PGPASS"))
