import asyncpg
from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.db.connection import get_connection_pool
from app.models.subscription import Subscription
from app.schemas.api_response import SubscriptionAPIResponse, SubscriptionsData

router = APIRouter()


@router.get("/{guild_id}/subscriptions", response_model=SubscriptionAPIResponse)
async def list_guild_subscriptions_api(
        guild_id: int,
        _auth=Security(verify_all_tokens)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch("SELECT * FROM subscriptions WHERE guild_id = $1", guild_id)
        subscriptions = []
        for row in res:
            subscription = Subscription.from_dict(dict(row))
            subscriptions.append(subscription)
    return SubscriptionAPIResponse(
        message="Fetched subscriptions.",
        data=SubscriptionsData(
            subscriptions=subscriptions
        )
    )
