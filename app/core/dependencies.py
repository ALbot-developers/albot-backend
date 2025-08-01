# サブスクリプションの取得
import asyncpg
from fastapi import Request, Header

from app.core.auth import verify_turnstile_token
from app.db.connection import get_connection_pool
from app.models.subscription import Subscription


async def get_subscription(request: Request, guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE guild_id = $1', guild_id)
    return Subscription.from_dict(dict(row)) if row else None


async def verify_turnstile(turnstile_token: str = Header(..., description="Cloudflare Turnstile token")):
    """Dependency to verify turnstile token from request header"""
    await verify_turnstile_token(turnstile_token)
    return True
