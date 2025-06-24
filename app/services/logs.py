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


async def record_character_usage(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO log.character_count_history (guild_id, wavenet_usage, standard_usage) SELECT guild_id, wavenet_count_now, standard_count_now FROM word_count WHERE guild_id = $1',
            guild_id
        )


async def record_connection_event(guild_id: int, event: Literal['connect', 'disconnect']):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO log.connection_events (guild_id, event) VALUES ($1, $2)',
            guild_id, event
        )
