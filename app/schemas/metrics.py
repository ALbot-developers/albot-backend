from typing import Optional

from pydantic import BaseModel


class Metrics(BaseModel):
    connected: bool
    guilds: int


class MetricsPost(BaseModel):
    connected: Optional[int] = None
    guilds: Optional[int] = None
