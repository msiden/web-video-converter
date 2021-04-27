from fastapi import FastAPI, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
from video_converter.bitrate_converter import BitRateConverter
from video_converter.schemas import Items, BitRate
from video_converter.file_manager import *


br_converter = BitRateConverter()
app = FastAPI()
app.mount("/static", StaticFiles(directory="frontend/"), name="static")
app.mount("/img", StaticFiles(directory="frontend/img/"), name="img")
app.mount("/js", StaticFiles(directory="frontend/js/"), name="js")
templates = Jinja2Templates(directory="frontend/")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    save_files(files)
    #return {"filenames": [file.filename for file in files]}


@app.post("/add")
def add_to_queue(items: Items) -> None:
    br_converter.add_to_queue(items.files)


@app.get("/queue")
def get_queue() -> list:
    return br_converter.get_queue()


@app.delete("/clear")
def clear_queue() -> None:
    br_converter.clear_queue()


@app.get("/in_progress")
def get_progress() -> list:
    return br_converter.get_progress()


@app.get("/done")
def get_done_items() -> list:
    return br_converter.get_done_items()


@app.get("/failed")
def get_failed_items() -> list:
    return br_converter.get_failed_items()


@app.put("/set_bitrate")
def set_bitrate(new_bitrate: BitRate) -> None:
    br_converter.set_bitrate(new_bitrate.bitrate)


@app.get("/bitrate")
def get_bitrate() -> str:
    return br_converter.get_bitrate()


@app.post("/process")
def process_queue():
    return br_converter.process_queue()
