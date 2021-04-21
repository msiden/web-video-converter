from pydantic import BaseModel
from typing import List


class Items(BaseModel):
    files: List[str]


class BitRate(BaseModel):
    bitrate: int
