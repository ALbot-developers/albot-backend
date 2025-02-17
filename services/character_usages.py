import json
from typing import Union, Literal

import asyncpg

from db.connection import get_connection_pool
from models.api_response import CharacterUsages, CharacterUsage


async def get(guild_id: int) -> CharacterUsages:
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow(
            'SELECT '
            'wavenet_count_now, standard_count_now, limit_word_count '
            'FROM word_count WHERE guild_id = $1',
            guild_id
        )
        if not row:
            # 無課金サーバーのデフォルト値
            return CharacterUsages(
                wavenet=CharacterUsage(monthly_quota=5000, used_characters=0),
                standard=CharacterUsage(monthly_quota=5000, used_characters=0)
            )
        quotas = json.loads(row['limit_word_count'])
        wavenet = CharacterUsage(
            monthly_quota=quotas["wavenet"],
            used_characters=row['wavenet_count_now']
        )
        standard = CharacterUsage(
            monthly_quota=quotas["standard"],
            used_characters=row['standard_count_now']
        )
    return CharacterUsages(wavenet=wavenet, standard=standard)


async def update(guild_id: int, voice_type: Union[Literal["wavenet"], Literal["standard"]], payload: CharacterUsage):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if voice_type == "wavenet":
            await conn.execute(
                '''
                INSERT INTO 
                    word_count (wavenet_count_now, guild_id) 
                VALUES
                    ($1, $2) 
                ON CONFLICT (guild_id) 
                    DO UPDATE SET wavenet_count_now = $1
                ''',
                payload.used_characters, guild_id
            )
        else:
            await conn.execute(
                '''
                INSERT INTO 
                    word_count (standard_count_now, guild_id) 
                VALUES
                    ($1, $2) 
                ON CONFLICT (guild_id) 
                    DO UPDATE SET standard_count_now = $1
                ''',
                payload.used_characters, guild_id
            )
