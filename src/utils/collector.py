import os


def flush(file_path: str) -> None:
    try:
        os.remove(file_path)
    except RuntimeError:
        print("No such file")
