import ffmpeg
from copy import copy


FILE_NAME_SUFFIX = "({}bps).mp4"


class BitRateConverter(object):

    def __init__(self):
        self.__queue = set()
        self.__bitrate = 8

    def add_to_queue(self, items: list) -> None:
        self.__queue.update(items)

    def get_queue(self) -> list:
        return list(self.__queue)

    def clear_queue(self) -> None:
        self.__queue.clear()

    def remove_from_queue(self, item: str) -> None:
        self.__queue.remove(item)

    def set_bitrate(self, new_bitrate: int) -> None:
        self.__bitrate = new_bitrate

    def get_bitrate(self) -> str:
        return f"{self.__bitrate}M"

    def process_queue(self) -> None:
        queue = copy(self.get_queue())
        for file_ in queue:
            success = self.process_item(file_)
            if success:
                self.remove_from_queue(file_)

    def process_item(self, path: str) -> bool:
        output_file = path[:path.rfind(".")] + FILE_NAME_SUFFIX.format(self.get_bitrate())
        stream = ffmpeg.input(path)
        stream = ffmpeg.output(stream, output_file, video_bitrate=self.get_bitrate())
        try:
            ffmpeg.run(stream, quiet=True)
            return True
        except ffmpeg.Error:
            return False


