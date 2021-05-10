import shutil
from zipfile import ZipFile
from fastapi import UploadFile
from typing import List
from video_converter.constants import *
from video_converter.utils import *


class FileManager(object):

    def __init__(self, token):
        self.token = token
        self.UPLOADS_DIRECTORY = UPLOADS_DIRECTORY.format(token)
        self.COMPLETED_DIRECTORY = COMPLETED_DIRECTORY.format(token)
        self.USER_DIRECTORY = USER_ROOT.format(token)
        self.ZIP_FILE = ZIP_FILE.format(token)
        create_directory(self.UPLOADS_DIRECTORY)
        create_directory(self.COMPLETED_DIRECTORY)

    def __save_uploadfile(self, file: UploadFile) -> str:
        file_name = self.UPLOADS_DIRECTORY + file.filename
        with open(file_name, "w+b") as f:
            shutil.copyfileobj(file.file, f)
        return file_name

    def save_files_from_upload(self, files: List[UploadFile]) -> list:
        file_names = []
        for file in files:
            file_name = self.__save_uploadfile(file)
            file_names.append(file_name)
        return file_names

    def get_uploads(self) -> list:
        return os.listdir(self.UPLOADS_DIRECTORY)

    def get_completed_files(self) -> List[str]:
        return [self.COMPLETED_DIRECTORY + f for f in os.listdir(self.COMPLETED_DIRECTORY)]

    def delete_user_files(self) -> None:
        delete_directory(self.USER_DIRECTORY)

    def delete_uploads(self) -> None:
        delete_directory(self.UPLOADS_DIRECTORY)

    def zip_completed_files(self) -> None:
        with ZipFile(self.ZIP_FILE, "w") as zipfile:
            for file in self.get_completed_files():
                if file.endswith(".zip"):
                    continue
                zipfile.write(file)
