import asyncpg

from app.db.connection import get_connection_pool


async def create(guild_id):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO settings_data (guild_id) VALUES ($1) ON CONFLICT DO NOTHING',
            guild_id
        )
        # memo: word_countへの挿入はとりあえず行わない
        # await conn.execute(
        #     'INSERT INTO word_count (guild_id) VALUES ($1) ON CONFLICT DO NOTHING',
        #     guild_id
        # )


async def delete(guild_id):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # memo: word countは削除しない
        await conn.execute('DELETE FROM settings_data WHERE guild_id = $1', guild_id)
