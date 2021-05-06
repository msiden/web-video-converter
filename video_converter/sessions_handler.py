import uuid
from video_converter.process_handler import ProcessHandler


class SessionsHandler(object):

    def __init__(self):
        self.sessions = {}

    def new(self):
        token = self.get_token()
        self.sessions.update({f"uuid={token}": ProcessHandler()})
        return token

    @staticmethod
    def get_token():
        return str(uuid.uuid4())
