from enum import Enum, auto


class VideoFileStatus(Enum):
    IN_QUEUE = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    FAILED = auto()
