import datetime
import json

import asyncpg

from app.db.connection import get_connection_pool
from app.external.discord.models import PartialGuild


async def get_guilds(user_id: int, mutual=True) -> list[PartialGuild]:
    if mutual:
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            rows: list = await conn.fetch(
                '''
                WITH expanded_guilds AS (
                    SELECT jsonb_array_elements(guilds) AS guild
                    FROM user_guilds
                    WHERE user_id = $1
                )
                SELECT eg.guild
                FROM expanded_guilds eg
                JOIN settings_data sd 
                ON sd.guild_id::text = eg.guild->>'id';
                ''',
                user_id
            )
        return [PartialGuild.from_dict(json.loads(row["guild"])) for row in rows]
    else:
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            guilds = await conn.fetchval(
                'SELECT guilds FROM user_guilds WHERE user_id = $1',
                user_id
            )
        return [PartialGuild.from_dict(guild) for guild in json.loads(guilds)]


async def store_guilds(user_id: int, guilds: list[PartialGuild]):
    dict_guilds = [guild.to_dict() for guild in guilds]
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO user_guilds (user_id, guilds, updated_at) VALUES ($1, $2, $3) '
            'ON CONFLICT (user_id) DO UPDATE SET guilds = $2, updated_at = $3',
            user_id, json.dumps(dict_guilds), datetime.datetime.now()
        )


async def get_guild(user_id: int, guild_id: int) -> PartialGuild:
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        guild: str | None = await conn.fetchval(
            '''
            WITH expanded_guilds AS (
                SELECT jsonb_array_elements(guilds) AS guild
                FROM user_guilds
                WHERE user_id = $1
            )
            SELECT eg.guild
            FROM expanded_guilds eg
            WHERE eg.guild->>'id' = $2;
            ''',
            int(user_id), str(guild_id)
        )
        return PartialGuild.from_dict(json.loads(guild)) if guild else None
