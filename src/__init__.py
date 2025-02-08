from src.core.config import settings

if __name__ == "__main__":
    print(settings.log_file_path.joinpath("outer.log"))
