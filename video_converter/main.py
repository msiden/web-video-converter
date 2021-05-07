from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from threading import Thread
from video_converter.schemas import Items, BitRate
from video_converter.constants import *
from video_converter.sessions_handler import SessionsHandler
from video_converter.utils import *

# TODO!
# user session files are not deleted when session expires
# The whole user_files directory should be deleted when program ends
# Don't extract token from request for each function below. Move this to session.call.

create_directory(FILES_ROOT)

session = SessionsHandler()
app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/"), name="static")
app.mount("/img", StaticFiles(directory="frontend/img/"), name="img")
app.mount("/js", StaticFiles(directory="frontend/js/"), name="js")
app.mount("/user_files", StaticFiles(directory="user_files/"), name="user_files")
templates = Jinja2Templates(directory="frontend/")

sessions_daemon = Thread(target=session.daemon, args=(), daemon=True)
sessions_daemon.start()


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> templates.TemplateResponse:
    response = templates.TemplateResponse("index.html", {"request": request})
    token = get_token()
    response.set_cookie(key="uuid", value=token)
    return response


@app.get("/token")
def get_token() -> str:
    return session.new()


@app.post("/upload")
def upload_files(request: Request, files: List[UploadFile] = File(...)) -> None:
    token = request.headers.get("cookie")
    session.call(token).upload_files(files)


@app.get("/download")
def get_download_link(request: Request) -> str:
    token = request.headers.get("cookie")
    return HOME_URL + ZIP_FILE.format(token)


@app.get("/completed_files")
def get_completed_files(request: Request) -> list:
    token = request.headers.get("cookie")
    return session.call(token).get_download_link()


@app.post("/add")
def add_to_queue(request: Request, items: Items) -> None:
    token = request.headers.get("cookie")
    session.call(token).add_to_queue(items.files)


@app.get("/queue")
def get_queue(request: Request) -> list:
    token = request.headers.get("cookie")
    return session.call(token).get_queue()


@app.delete("/clear")
def clear_queue(request: Request) -> None:
    token = request.headers.get("cookie")
    session.call(token).clear_queue()


@app.get("/in_progress")
def get_progress(request: Request) -> list:
    token = request.headers.get("cookie")
    return session.call(token).get_progress()


@app.get("/done")
def get_done_items(request: Request) -> list:
    token = request.headers.get("cookie")
    return session.call(token).get_done_items()


@app.get("/failed")
def get_failed_items(request: Request) -> list:
    token = request.headers.get("cookie")
    return session.call(token).get_failed_items()


@app.put("/set_bitrate")
def set_bitrate(request: Request, new_bitrate: BitRate) -> None:
    token = request.headers.get("cookie")
    session.call(token).set_bitrate(new_bitrate.bitrate)


@app.get("/bitrate")
def get_bitrate(request: Request) -> str:
    token = request.headers.get("cookie")
    return session.call(token).get_bitrate()


@app.post("/process")
def process_queue(request: Request) -> None:
    token = request.headers.get("cookie")
    return session.call(token).process_queue()
