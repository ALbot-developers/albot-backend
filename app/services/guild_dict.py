import json

import asyncpg

from app.db.connection import get_connection_pool


async def get(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        value = await conn.fetchval('SELECT dict FROM dict_data WHERE guild_id = $1', guild_id)
    return json.loads(value) if value is not None else {}


async def delete(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを削除
        await conn.execute('DELETE FROM dict_data WHERE guild_id = $1', guild_id)


async def update(guild_id: int, value: dict):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # remove empty values
        new_dict = {k: v for k, v in value.items() if k and v}
        # guild_idのデータを更新
        await conn.execute('''
        INSERT INTO dict_data (dict, guild_id) VALUES ($1, $2)
        ON CONFLICT (guild_id) DO UPDATE SET dict = $1
        ''', json.dumps(new_dict), guild_id)
