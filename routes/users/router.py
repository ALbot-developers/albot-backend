from fastapi import APIRouter

from routes.users import subscriptions_api

router = APIRouter()

router.include_router(subscriptions_api.router, prefix="/me/subscriptions")
