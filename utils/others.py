import json

import asyncpg

from type_specifications.discord_api import PartialGuild
from utils.db_connection import get_connection_pool


async def get_user_guilds(user_id: int) -> list[PartialGuild]:
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
