from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from video_converter.handler import Handler
from video_converter.schemas import Items, BitRate


handler = Handler()
app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/"), name="static")
app.mount("/img", StaticFiles(directory="frontend/img/"), name="img")
app.mount("/js", StaticFiles(directory="frontend/js/"), name="js")
templates = Jinja2Templates(directory="frontend/")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)) -> None:
    handler.upload_files(files)


@app.get("/download")
def get_download_link() -> list:
    return handler.get_download_link()


@app.post("/add")
def add_to_queue(items: Items) -> None:
    handler.add_to_queue(items.files)


@app.get("/queue")
def get_queue() -> list:
    return handler.get_queue()


@app.delete("/clear")
def clear_queue() -> None:
    handler.clear_queue()


@app.get("/in_progress")
def get_progress() -> list:
    return handler.get_progress()


@app.get("/done")
def get_done_items() -> list:
    return handler.get_done_items()


@app.get("/failed")
def get_failed_items() -> list:
    return handler.get_failed_items()


@app.put("/set_bitrate")
def set_bitrate(new_bitrate: BitRate) -> None:
    handler.set_bitrate(new_bitrate.bitrate)


@app.get("/bitrate")
def get_bitrate() -> str:
    return handler.get_bitrate()


@app.post("/process")
def process_queue():
    return handler.process_queue()
