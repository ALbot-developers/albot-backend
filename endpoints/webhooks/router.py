from fastapi import APIRouter

from endpoints.webhooks import stripe_webhook

router = APIRouter()

router.include_router(stripe_webhook.router, prefix="/stripe")
