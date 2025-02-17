# サブスクリプションの取得
import asyncpg
from fastapi import Request

from db.connection import get_connection_pool
from models.subscription import Subscription


async def get_subscription(request: Request, guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE guild_id = $1', guild_id)
    return Subscription.from_dict(dict(row)) if row else None
