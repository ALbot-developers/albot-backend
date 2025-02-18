from pydantic import BaseModel


class ConnectionCommand(BaseModel):
    command: str
