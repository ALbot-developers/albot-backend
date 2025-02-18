import datetime
from typing import Optional

from pydantic import BaseModel


class Subscription(BaseModel):
    user_id: int
    sub_start: datetime.date
    plan: str
    last_updated: datetime.date
    sub_id: str
    guild_id: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            user_id=data.get('user_id'),
            sub_start=data.get('sub_start'),
            plan=data.get('plan'),
            last_updated=data.get('last_updated'),
            sub_id=data.get('sub_id'),
            guild_id=data.get('guild_id')
        )
