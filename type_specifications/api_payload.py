from dataclasses import dataclass


@dataclass
class ActivateSubscriptionAPIPayload:
    guild_id: int


@dataclass
class RenewSubscriptionAPIPayload:
    guild_id: int
    new_plan: str
