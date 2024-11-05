from fastapi import APIRouter

import stripe_webhook

router = APIRouter()

router.include_router(stripe_webhook.router, prefix="/stripe")
