from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from video_converter.schemas import Items, BitRate
from video_converter.constants import *
from video_converter.sessions_handler import SessionsHandler


session = SessionsHandler()
app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/"), name="static")
app.mount("/img", StaticFiles(directory="frontend/img/"), name="img")
app.mount("/js", StaticFiles(directory="frontend/js/"), name="js")
app.mount("/completed", StaticFiles(directory="completed/"), name="completed")
templates = Jinja2Templates(directory="frontend/")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    token = session.new()
    response = templates.TemplateResponse("index.html", {"request": request})
    response.set_cookie(key="uuid", value=token)
    return response


@app.post("/upload")
def upload_files(request: Request, files: List[UploadFile] = File(...)) -> None:
    token = request.headers.get("cookie")
    print(token)
    session.sessions[token].upload_files(files)


@app.get("/download")
def get_download_link() -> str:
    return HOME_URL + ZIP_FILE


@app.get("/completed_files")
def get_completed_files(request: Request) -> list:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].get_download_link()


@app.post("/add")
def add_to_queue(request: Request, items: Items) -> None:
    token = request.headers.get("cookie")
    print(token)
    session.sessions[token].add_to_queue(items.files)


@app.get("/queue")
def get_queue(request: Request) -> list:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].handler.get_queue()


@app.delete("/clear")
def clear_queue(request: Request) -> None:
    token = request.headers.get("cookie")
    print(token)
    session.sessions[token].clear_queue()


@app.get("/in_progress")
def get_progress(request: Request) -> list:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].get_progress()


@app.get("/done")
def get_done_items(request: Request) -> list:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].get_done_items()


@app.get("/failed")
def get_failed_items(request: Request) -> list:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].get_failed_items()


@app.put("/set_bitrate")
def set_bitrate(request: Request, new_bitrate: BitRate) -> None:
    token = request.headers.get("cookie")
    print(token)
    session.sessions[token].set_bitrate(new_bitrate.bitrate)


@app.get("/bitrate")
def get_bitrate(request: Request) -> str:
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].get_bitrate()


@app.post("/process")
def process_queue(request: Request):
    token = request.headers.get("cookie")
    print(token)
    return session.sessions[token].process_queue()
