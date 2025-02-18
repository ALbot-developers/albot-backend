from typing import Optional

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


async def update(shard_id: int, connected: Optional[int] = None, guilds: Optional[int] = None):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if connected:
            await conn.execute(
                'UPDATE shard_data SET connected_num = $1 WHERE shard_id = $2',
                connected, shard_id
            )
        if guilds:
            await conn.execute(
                'UPDATE shard_data SET guilds_num = $1 WHERE shard_id = $2',
                guilds, shard_id
            )
