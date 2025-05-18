from typing import Literal

import asyncpg

from app.db.connection import get_connection_pool


async def record_guild_event(guild_id: int, event: Literal['join', 'leave']):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO log.guild_events (guild_id, event) VALUES ($1, $2)',
            guild_id, event
        )


async def record_character_usage(guild_id: int, character_count: int, voice_type: Literal['wavenet', 'standard']):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO log.character_count_usage (guild_id, voice_type, amount) VALUES ($1, $2, $3)',
            guild_id, voice_type, character_count
        )
