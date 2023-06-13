from typing import Any
from pydantic import BaseModel


class FileObject(BaseModel):
    name: str
    data: Any


class TextFileObject(BaseModel):
    name: str
    path: str
