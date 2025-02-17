from pydantic import BaseModel


class Metrics(BaseModel):
    connected: bool
    guilds: int
