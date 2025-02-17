import asyncpg

from app.db.connection import get_connection_pool
from app.schemas.metrics import Metrics


async def get():
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetchrow(
            "SELECT SUM(connected_num) as connected, SUM(guilds_num) as guilds FROM shard_data"
        )
    return Metrics.model_validate(dict(res))
