import shutil
import os
from fastapi import UploadFile
from typing import List
from video_converter.constants import *


class FileManager(object):

    def __init__(self):
        self.__create_directory(UPLOADS_DIRECTORY)
        self.__create_directory(COMPLETED_DIRECTORY)

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
        return os.listdir(COMPLETED_DIRECTORY)

    @staticmethod
    def delete_uploads():
        pass

    @staticmethod
    def delete_completed_files():
        pass

    def zip_files(self):
        pass