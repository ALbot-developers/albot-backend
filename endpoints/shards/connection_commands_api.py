import time

import asyncpg
from fastapi import APIRouter, Security

import constants
from core.auth import verify_bearer_token
from db.connection import get_connection_pool

router = APIRouter()


@router.get("/{shard_id}/connection_commands")
async def get_connection_commands(
        shard_id: int,
        changes_only: bool = False,
        _auth=Security(verify_bearer_token)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # todo: latest_command_fetch の命名を改善
        previously_updated_at: int = await conn.fetchval(
            'SELECT latest_command_fetch FROM shard_data WHERE shard_id = $1', shard_id
        )
        if changes_only:
            rows = await conn.fetch(
                'SELECT guild_id, command FROM connect_command WHERE (guild_id >> 22) % $1 = $2 AND connect_command.unix_last_update > $3',
                constants.SHARD_COUNT, shard_id, previously_updated_at
            )
        else:
            rows = await conn.fetch(
                'SELECT guild_id, command FROM connect_command WHERE (guild_id >> 22) % $1 = $2',
                constants.SHARD_COUNT, shard_id
            )
        await conn.execute(
            'UPDATE shard_data SET latest_command_fetch = $1 WHERE shard_id = $2',
            int(time.time()), shard_id
        )
    data = {}
    for row in rows:
        data[row["guild_id"]] = row["command"]
    return {
        "message": "Fetched connection commands.",
        "data": {
            "commands": data
        }
    }
