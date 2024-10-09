from typing import Dict, Literal

import asyncpg
from fastapi import APIRouter, Security

from utils.auth import verify_all_tokens
from utils.db_connection import get_connection_pool

router = APIRouter()


@router.get("/{guild_id}/message_link_expand_preference")
async def get_guild_message_link_expand_pref(guild_id: int, _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        value = await conn.fetchval('SELECT expand_message_link FROM settings_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Fetched guild data.",
        "data": {
            "enabled": value if value is not None else False
        }
    }


@router.post("/{guild_id}/message_link_expand_preference")
async def update_guild_message_link_expand_pref(guild_id: int, data: Dict[Literal["enabled"], bool],
                                                _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        enabled = data["enabled"]
        await conn.execute('UPDATE settings_data SET expand_message_link = $1 WHERE guild_id = $2', enabled, guild_id)
    return {
        "message": "Updated guild data."
    }
