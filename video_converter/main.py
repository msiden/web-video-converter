from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from threading import Thread
from video_converter.schemas import *
from video_converter.constants import *
from video_converter.sessions_handler import SessionsHandler
from video_converter.utils import *


create_directory(FILES_ROOT)

session = SessionsHandler()
sessions_daemon = Thread(target=session.daemon, args=(), daemon=True)
sessions_daemon.start()

app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/"), name="static")
app.mount("/img", StaticFiles(directory="frontend/img/"), name="img")
app.mount("/js", StaticFiles(directory="frontend/js/"), name="js")
app.mount("/user_files", StaticFiles(directory="user_files/"), name="user_files")
templates = Jinja2Templates(directory="frontend/")


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
    session.call(request).upload_files(files)


@app.get("/download")
def get_download_link(request: Request) -> str:
    token = request.headers.get("cookie")
    return HOME_URL + ZIP_FILE.format(token)


@app.get("/completed_files")
def get_completed_files(request: Request) -> list:
    return session.call(request).get_download_link()


@app.get("/queue")
def get_queue(request: Request) -> list:
    return session.call(request).get_queue()


@app.delete("/clear")
def clear_queue(request: Request) -> None:
    session.call(request).clear_queue()


@app.get("/in_progress")
def get_progress(request: Request) -> list:
    return session.call(request).get_progress()


@app.get("/done")
def get_done_items(request: Request) -> list:
    return session.call(request).get_done_items()


@app.get("/failed")
def get_failed_items(request: Request) -> list:
    return session.call(request).get_failed_items()


@app.put("/set_bitrate")
def set_bitrate(request: Request, new_bitrate: BitRate) -> None:
    session.call(request).set_bitrate(new_bitrate.bitrate)


@app.get("/bitrate")
def get_bitrate(request: Request) -> str:
    return session.call(request).get_bitrate()


@app.post("/process")
def process_queue(request: Request) -> None:
    return session.call(request).process_queue()
