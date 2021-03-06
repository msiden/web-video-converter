import uuid
import time
import atexit
from fastapi import HTTPException, status, Request
from video_converter.process_handler import ProcessHandler
from video_converter.utils import *
from video_converter.constants import *


class SessionsHandler(object):
    """Class for handling user sessions. Returns a unique instance of the process handler for each user connecting
    to the service"""

    def __init__(self):
        self.sessions = {}
        atexit.register(delete_directory, directory=FILES_ROOT)

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
        self.call(token=token).file_manager.delete_user_files()
        del self.sessions[token]

    @staticmethod
    def get_token() -> str:
        return str(uuid.uuid4())

    def call(self, request: Request = None, token: str = None) -> ProcessHandler:
        """Verify that the user has a valid session and route API calls to the process handler"""
        if request:
            cookie = request.headers.get("cookie")
            token = get_token_from_cookie(cookie)
        if token not in self.sessions:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")
        return self.sessions.get(token).get("handler")

    def daemon(self) -> None:
        """Continuously check for expired sessions and delete them"""
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
