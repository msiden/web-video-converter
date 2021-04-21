from fastapi import FastAPI
from bitrate_converter import BitRateConverter
from schemas import Items, BitRate


app = FastAPI()
br_converter = BitRateConverter()


@app.post("/add_to_queue")
def add_to_queue(items: Items) -> None:
    br_converter.add_to_queue(items.files)


@app.get("/get_queue")
def get_queue() -> list:
    return br_converter.get_queue()


@app.delete("/clear_queue")
def clear_queue() -> None:
    br_converter.clear_queue()


@app.put("/set_bitrate")
def set_bitrate(new_bitrate: BitRate) -> None:
    br_converter.set_bitrate(new_bitrate.bitrate)


@app.get("/get_bitrate")
def get_bitrate() -> int:
    return br_converter.get_bitrate()


@app.post("/process_queue")
def process_queue():
    return br_converter.process_queue()


