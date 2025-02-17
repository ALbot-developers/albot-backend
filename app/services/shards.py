from typing import Literal

import asyncpg
from fastapi import HTTPException

from app import constants
from app.db.connection import get_connection_pool
from app.models.shards import ProvisioningConfig


async def provision():
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # SQLクエリを実行
        # is_assignedがfalseのshard_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM shard_data WHERE is_assigned = false LIMIT 1')
        total_shards = await conn.fetchval('SELECT COUNT(*) FROM shard_data')
        if row is None:
            raise HTTPException(status_code=400, detail="No available shards.")
        # shard_idを取得
        shard_id = row['shard_id']
        tts_key = row["tts_key"]
        heartbeat_token = row["shardd_token"]
        # is_assignedをtrueに更新
        await conn.execute(
            'UPDATE shard_data SET is_assigned = true WHERE shard_id = $1', shard_id
        )
    return ProvisioningConfig(
        shard_count=total_shards,
        shard_id=shard_id,
        discord_token=constants.BOT_DISCORD_TOKEN,
        sentry_dsn=constants.SENTRY_DSN,
        tts_key=tts_key,
        heartbeat_token=heartbeat_token
    )


async def release(shard_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # is_assignedをfalseに更新
        await conn.execute(
            'UPDATE shard_data SET is_assigned = false WHERE shard_id = $1', shard_id
        )


async def list_ids(status: Literal["online", "offline", "all"]) -> list[int]:
    if status == "all":
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data"
            )
    elif status == "online":
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data WHERE is_assigned is true"
            )
    else:
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data WHERE is_assigned is false"
            )
    return [int(row[0]) for row in res]
