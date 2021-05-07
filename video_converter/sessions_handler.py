import uuid
import time
from fastapi import HTTPException, status
from video_converter.process_handler import ProcessHandler
from video_converter.utils import *
from video_converter.constants import *


class SessionsHandler(object):

    def __init__(self):
        self.sessions = {}

    def new(self) -> str:
        token = self.get_token()
        create_directory(USER_ROOT.format(token))
        self.sessions.update({
            f"uuid={token}": {
                "handler": ProcessHandler(token), "time_stamp": int(time.time())
            }
        })
        return token

    def delete(self, token: str) -> None:
        del self.sessions[token]

    @staticmethod
    def get_token() -> str:
        return str(uuid.uuid4())

    def call(self, token: str) -> ProcessHandler:
        if token not in self.sessions:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return self.sessions.get(token).get("handler")

    def daemon(self) -> None:
        while True:
            now = time.time()
            sessions = {
                token: self.sessions.get(token).get("time_stamp")
                for token in self.sessions
            }

            for session in sessions:
                time_stamp = sessions.get(session)
                session_has_expired = time_stamp + SESSION_DURATION < now

                if session_has_expired:
                    self.delete(session)

            time.sleep(SESSION_DAEMON_INTERVAL)
