import json

import asyncpg
from fastapi import APIRouter, Security

from models.api_response import CharacterUsageAPIResponse, CharacterUsage, CharacterUsages
from utils.auth import verify_all_tokens, verify_bearer_token
from utils.db_connection import get_connection_pool

router = APIRouter()


async def get_guild_character_usage(guild_id: int):
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


@router.get("/{guild_id}/character_usage", response_model=CharacterUsageAPIResponse)
async def get_guild_character_usage_api(guild_id: int, _auth=Security(verify_all_tokens)):
    return CharacterUsageAPIResponse(
        message="Fetched guild data.",
        data=await get_guild_character_usage(guild_id)
    )


@router.post("/{guild_id}/character_usage")
async def update_guild_character_usage(
        guild_id: int, payload: CharacterUsages,
        _auth=Security(verify_bearer_token)
):
    # update used characters
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if payload.wavenet:
            await conn.execute(
                '''
                INSERT INTO 
                    word_count (wavenet_count_now, guild_id) 
                VALUES
                    ($1, $2) 
                ON CONFLICT (guild_id) 
                    DO UPDATE SET wavenet_count_now = $1
                ''',
                payload.wavenet.used_characters, guild_id
            )
        if payload.standard:
            await conn.execute(
                '''
                INSERT INTO 
                    word_count (standard_count_now, guild_id) 
                VALUES
                    ($1, $2) 
                ON CONFLICT (guild_id) 
                    DO UPDATE SET standard_count_now = $1
                ''',
                payload.standard.used_characters, guild_id
            )
    return {
        "message": "Updated guild data."
    }
