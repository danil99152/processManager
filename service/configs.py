from datetime import datetime

from pydantic import BaseModel


class App(BaseModel):
    pid: int
    name: str
    cpu_percent: str
    memory_percent: str
    opened_at: datetime


class History(BaseModel):
    pid: int
    name: str
    opened_at: datetime
    closed_at: datetime
