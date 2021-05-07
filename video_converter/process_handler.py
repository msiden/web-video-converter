from video_converter.pool import *
from video_converter.file_manager import FileManager
from video_converter.bitrate_converter import BitRateConverter


class ProcessHandler(object):

    def __init__(self, token: str):
        self.__bitrate = 8
        self.br_converter = BitRateConverter()
        self.file_manager = FileManager(token)
        self.pool = Pool()
        self.queue = self.pool.queue
        self.in_progress = self.pool.in_progress
        self.done_items = self.pool.done
        self.failed_items = self.pool.failed
        self.token = token

    def add_to_queue(self, items: list or str) -> None:
        self.queue.add(items)

    def get_queue(self) -> list:
        return self.queue.files()

    def clear_queue(self) -> None:
        self.queue.clear()
        self.file_manager.delete_uploads()

    def get_progress(self) -> list:
        return self.in_progress.files()

    def get_done_items(self) -> list:
        return self.done_items.files()

    def get_failed_items(self) -> list:
        return self.failed_items.files()

    def upload_files(self, files: list) -> None:
        file_names = self.file_manager.save_files_from_upload(files)
        self.add_to_queue(file_names)

    def set_bitrate(self, new_bitrate: int) -> None:
        self.__bitrate = new_bitrate

    def get_bitrate(self) -> str:
        return f"{self.__bitrate}M"

    def process_queue(self) -> None:
        for item in self.queue.content():
            self.pool.update_item_status(item)
            passed = self.br_converter.process_item(item, self.get_bitrate())
            self.pool.update_item_status(item, passed=passed)
        self.file_manager.zip_completed_files()

    def get_download_link(self) -> list:
        return self.file_manager.get_completed_files()
