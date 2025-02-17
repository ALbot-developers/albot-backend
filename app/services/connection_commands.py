import time

import asyncpg

from app import constants
from app.core.error import CustomHTTPException
from app.db.connection import get_connection_pool

EXISTING_COMMANDS = ("t.help", "t.id", "t.status", "t.expand", "t.act", "t.dict", "t.view", "t.save", "t.dc")


async def get_by_guild(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        command: str = await conn.fetchval(
            'SELECT command FROM connect_command WHERE guild_id = $1', guild_id
        )
    return command


async def get_by_shard(shard_id: int, changes_only: bool):
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
    return {row['guild_id']: row['command'] for row in rows}


async def update(guild_id: int, command: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        for _ in EXISTING_COMMANDS:
            if _.startswith(command):
                raise CustomHTTPException(
                    status_code=400,
                    detail="Command already exists."
                )
        # upsert
        await conn.execute(
            'INSERT INTO connect_command (guild_id, command) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET command = $2',
            guild_id, command
        )
