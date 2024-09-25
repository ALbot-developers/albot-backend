from dataclasses import dataclass


@dataclass
class SubscriptionAPIPayload:
    guild_id: int = None
