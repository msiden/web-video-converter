import shutil
import os
import atexit
from zipfile import ZipFile
from fastapi import UploadFile
from typing import List
from video_converter.constants import *


class FileManager(object):

    def __init__(self):
        self.__create_directory(UPLOADS_DIRECTORY)
        self.__create_directory(COMPLETED_DIRECTORY)
        atexit.register(self.delete_completed)
        atexit.register(self.delete_uploads)

    @staticmethod
    def __save_uploadfile(file: UploadFile) -> str:
        file_name = UPLOADS_DIRECTORY + file.filename
        with open(file_name, "w+b") as f:
            shutil.copyfileobj(file.file, f)
        return file_name

    @staticmethod
    def __create_directory(path):
        if not os.path.exists(path):
            os.mkdir(path)

    @staticmethod
    def __delete_all_files_in_directory(directory: str) -> None:
        for file in os.listdir(directory):
            os.remove(directory + file)

    def save_files_from_upload(self, files: List[UploadFile]) -> list:
        file_names = []
        for file in files:
            file_name = self.__save_uploadfile(file)
            file_names.append(file_name)
        return file_names

    @staticmethod
    def get_uploads() -> list:
        return os.listdir(UPLOADS_DIRECTORY)

    @staticmethod
    def get_completed_files() -> list:
        return [COMPLETED_DIRECTORY + f for f in os.listdir(COMPLETED_DIRECTORY)] + [COMPLETED_DIRECTORY + "test_file.zip"]

    def delete_uploads(self) -> None:
        self.__delete_all_files_in_directory(UPLOADS_DIRECTORY)

    def delete_completed(self) -> None:
        self.__delete_all_files_in_directory(COMPLETED_DIRECTORY)

    def zip_completed_files(self) -> None:
        with ZipFile(ZIP_FILE, "w") as zipfile:
            for file in self.get_completed_files():
                zipfile.write(COMPLETED_DIRECTORY + file)
