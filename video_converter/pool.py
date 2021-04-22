from enums import VideoFileStatus


FILE_NAME_SUFFIX = "({}bps).mp4"


class VideoFile(object):

    def __init__(self, path: str):
        self.status = VideoFileStatus.IN_QUEUE
        self.path = path
        self.output = path[:path.rfind(".")] + FILE_NAME_SUFFIX

    def is_in_queue(self) -> bool:
        return self.status == VideoFileStatus.IN_QUEUE

    def is_in_progress(self) -> bool:
        return self.status == VideoFileStatus.IN_PROGRESS

    def is_done(self) -> bool:
        return self.status == VideoFileStatus.DONE

    def failed(self) -> bool:
        return self.status == VideoFileStatus.FAILED

    def update_status(self, passed: bool = True) -> None:
        if self.is_in_queue():
            self.status = VideoFileStatus.IN_PROGRESS
        elif self.is_in_progress():
            self.status = VideoFileStatus.DONE if passed else VideoFileStatus.FAILED


class Queue(object):

    def __init__(self):
        self.__items = set()

    def add(self, items: list or str or VideoFile) -> None:
        items = [items] if type(items) in (VideoFile, str) else items
        for item in items:
            self.__items.add(VideoFile(item) if isinstance(item, str) else item)

    def clear(self):
        self.__items.clear()

    def remove(self, items: list or VideoFile) -> None:
        items = [items] if isinstance(items, VideoFile) else items
        for item in items:
            self.__items.remove(item)

    def files(self) -> list:
        return [item.path for item in self.__items]

    def content(self) -> list:
        return list(self.__items)


class Pool(object):

    def __init__(self):
        self.queue = Queue()
        self.in_progress = Queue()
        self.done = Queue()
        self.failed = Queue()

    def update_item_status(self, item: VideoFile, passed: bool = True) -> None:

        if item.is_in_queue():
            self.queue.remove(item)
        elif item.is_in_progress():
            self.in_progress.remove(item)

        item.update_status(passed=passed)

        if item.is_in_progress():
            self.in_progress.add(item)
        elif item.is_done():
            self.done.add(item)
        elif item.failed():
            self.failed.add(item)

