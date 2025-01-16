"""
Request Model
"""
from pydantic import BaseModel


class Request(BaseModel):
    path: str
    iz: str
    region: str
