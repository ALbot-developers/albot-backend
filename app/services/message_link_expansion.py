import asyncpg

from app.db.connection import get_connection_pool


async def is_enabled(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        value = await conn.fetchval(
            'SELECT expand_message_link FROM settings_data WHERE guild_id = $1', guild_id
        )
    return value


async def set_enabled(guild_id: int, enabled: bool):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        await conn.execute('''
        INSERT INTO
            settings_data (expand_message_link, guild_id)
        VALUES 
            ($1, $2)
        ON CONFLICT 
            (guild_id)
        DO UPDATE SET 
            expand_message_link = $1
        ''', enabled, guild_id)
