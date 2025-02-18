from pydantic import BaseModel


class SubscriptionActivate(BaseModel):
    guild_id: int


class SubscriptionRenew(BaseModel):
    new_plan: str
