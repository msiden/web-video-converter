import ffmpeg
from video_converter.pool import *
from file_manager import FileManager


class BitRateConverter(object):

    def __init__(self):
        self.__bitrate = 8
        self.file_manager = FileManager()
        self.pool = Pool()
        self.queue = self.pool.queue
        self.in_progress = self.pool.in_progress
        self.done_items = self.pool.done
        self.failed_items = self.pool.failed

    def add_to_queue(self, items: list or str) -> None:
        self.queue.add(items)

    def get_queue(self) -> list:
        return self.queue.files()

    def clear_queue(self) -> None:
        self.queue.clear()

    def get_progress(self) -> list:
        return self.in_progress.files()

    def get_done_items(self) -> list:
        return self.done_items.files()

    def get_failed_items(self) -> list:
        return self.failed_items.files()

    def set_bitrate(self, new_bitrate: int) -> None:
        self.__bitrate = new_bitrate

    def get_bitrate(self) -> str:
        return f"{self.__bitrate}M"

    def upload_files(self, files: list) -> None:
        file_names = self.file_manager.save_files_from_upload(files)
        self.add_to_queue(file_names)

    def process_queue(self) -> None:
        for item in self.queue.content():
            self.process_item(item)

    def process_item(self, item: VideoFile) -> None:
        passed = True
        output_file = item.output.format(self.get_bitrate())
        stream = ffmpeg.input(item.path)
        stream = ffmpeg.output(stream, output_file, video_bitrate=self.get_bitrate())
        self.pool.update_item_status(item)
        try:
            ffmpeg.run(stream, quiet=True)
        except ffmpeg.Error:
            passed = False
        self.pool.update_item_status(item, passed=passed)
