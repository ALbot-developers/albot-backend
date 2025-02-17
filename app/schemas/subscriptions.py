import datetime
from dataclasses import dataclass


@dataclass
class SubscriptionData:
    guild_id: int
    user_id: int
    sub_id: str
    sub_start: datetime.date
    plan: str
    last_updated: datetime.date

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            guild_id=data.get('guild_id'),
            user_id=data.get('user_id'),
            sub_id=data.get('sub_id'),
            sub_start=data.get('sub_start'),
            plan=data.get('plan'),
            last_updated=data.get('last_updated')
        )
