
# https://fastapi.tiangolo.com/tutorial/request-files/
# https://siddharth1.medium.com/temp-files-and-tempfile-module-in-python-with-examples-570b4ee96a38

def save_files(files):
    for file in files:
        print(file.filename)
        print(file.content_type)
        print(file.file.read)
        with open(file.filename, "w+b") as f:
            f.write(file.file)
