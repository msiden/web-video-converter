from fastapi import FastAPI
from bitrate_converter import BitRateConverter

app = FastAPI()
br_converter = BitRateConverter()

# pydantic!
@app.post("/add_to_queue")
def add_to_queue(items: str):
    return br_converter.add_to_queue(items)


@app.get("/get_queue")
def get_queue() -> list:
    return br_converter.get_queue()


@app.post("/process_queue")
def process_queue():
    return "done"


@app.put("/set_bitrate")
def set_bitrate(new_bitrate: int):
    return
