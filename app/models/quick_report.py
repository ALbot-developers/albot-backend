from pydantic import BaseModel


class QuickReport(BaseModel):
    id: str
    guild_id: int
    category: str
    reported_at: str
    description: str
