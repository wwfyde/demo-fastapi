import os
import sys
from pathlib import Path

# import requests
from dotenv import load_dotenv, find_dotenv

if __name__ == '__main__':
    # requests.get(url="https://www.google.com")
    print(__package__)
    print(sys.path)
    # # Not Recommended use finde_dotenv instead
    # env_path = Path('.').absolute().parent.joinpath('.env')
    # load_dotenv(env_path)
    # with open(env_path) as f:
    #     for line in f:
    #         print(line.strip(), end='')
    # print(env_path)

    load_dotenv(find_dotenv())
    print(os.getenv('PGUSER'), os.getenv("PGPASS"))
