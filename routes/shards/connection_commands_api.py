import asyncpg
from fastapi import APIRouter, Security

import envs
from utils.auth import verify_token
from utils.db_connection import get_connection_pool

router = APIRouter()


@router.get("/{shard_id}/connection_commands")
async def get_connection_commands(shard_id: int, _auth=Security(lambda: verify_token("bearer"))):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # shard_idのデータを取得
        rows = await conn.fetch(
            'SELECT guild_id, command FROM connect_command WHERE (guild_id >> 22) % $1 = $2',
            envs.SHARD_COUNT, shard_id
        )
    data = {}
    for row in rows:
        data[row["guild_id"]] = row["command"]
    return {
        "message": "Fetched connection commands.",
        "data": data
    }
