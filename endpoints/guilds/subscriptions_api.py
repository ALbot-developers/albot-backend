import asyncpg
from fastapi import APIRouter, Security

from models.database import SubscriptionData
from utils.auth import verify_all_tokens
from utils.db_connection import get_connection_pool

router = APIRouter()


@router.get("/{guild_id}/subscriptions")
async def list_guild_subscriptions_api(
        guild_id: int,
        _auth=Security(verify_all_tokens)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch("SELECT * FROM subscriptions WHERE guild_id = $1", guild_id)
        subscriptions = []
        for row in res:
            subscription = SubscriptionData.from_dict(dict(row))
            subscriptions.append(subscription)
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": subscriptions
        }
    }
