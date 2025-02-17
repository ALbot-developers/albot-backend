from fastapi import APIRouter

from app.routes.webhooks import stripe_webhook

router = APIRouter()

router.include_router(stripe_webhook.router, prefix="/stripe")
