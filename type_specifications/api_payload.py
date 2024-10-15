from dataclasses import dataclass


@dataclass
class ActivateSubscriptionAPIPayload:
    guild_id: int


@dataclass
class RenewSubscriptionAPIPayload:
    new_plan: str


@dataclass
class CheckoutSessionAPIPayload:
    plan: str
