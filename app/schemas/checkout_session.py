from pydantic import BaseModel


class CheckoutSessionCreate(BaseModel):
    plan: str
