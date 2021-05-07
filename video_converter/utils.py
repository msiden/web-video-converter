import os


def create_directory(path: str) -> None:
    if not os.path.exists(path):
        os.mkdir(path)


def delete_directory(directory: str) -> None:

    items = os.listdir(directory)

    for item in items:
        item = directory + os.sep + item
        if os.path.isdir(item):
            delete_directory(item)
        elif os.path.isfile(item):
            os.remove(item)
    os.rmdir(directory)

