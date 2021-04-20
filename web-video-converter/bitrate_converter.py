import ffmpeg


class BitRateConverter(object):

    def __init__(self):
        self.__queue = set()
        self.__bitrate = 8

    def set_bitrate(self, new_bitrate: int) -> int:
        assert isinstance(new_bitrate, int), "Bitrate must be an integer value"
        return self.get_bitrate()

    def get_bitrate(self) -> int:
        return self.__bitrate

    def add_to_queue(self, items: str) -> list:
        items = items.split(",")
        self.__queue.update(items)
        return self.get_queue()

    def get_queue(self) -> list:
        return list(self.__queue)

    def empty_queue(self) -> list:
        self.__queue.clear()
        return self.get_queue()

    def process_queue(self):
        pass

    def process_item(self, file_name):
        suffix = "_(bitrate_{}).mp4".format(self.__bitrate)
        was_processed = True
        output_file = file_name[:file_name.rfind(".")] + suffix
        stream = ffmpeg.input(file_name)
        stream = ffmpeg.output(stream, output_file, video_bitrate=self.__bitrate)
        try:
            ffmpeg.run(stream, quiet=True)
        except ffmpeg.Error:
            was_processed = False
        return was_processed
