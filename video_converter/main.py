from fastapi import FastAPI
from bitrate_converter import BitRateConverter
from schemas import Items, BitRate


app = FastAPI()
br_converter = BitRateConverter()


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