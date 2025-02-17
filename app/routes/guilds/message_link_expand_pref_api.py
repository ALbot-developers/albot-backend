import asyncpg
from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.db.connection import get_connection_pool
from app.schemas.api_response import MessageLinkExpandAPIResponse, PlainAPIResponse
from app.schemas.message_link_expand_pref import MessageLinkExpansionPreference

router = APIRouter()


@router.get("/{guild_id}/message_link_expand_preference", response_model=MessageLinkExpandAPIResponse)
async def get_guild_message_link_expand_pref(guild_id: int, _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        value = await conn.fetchval('SELECT expand_message_link FROM settings_data WHERE guild_id = $1', guild_id)
    return MessageLinkExpandAPIResponse(
        message="Fetched guild data.",
        data=MessageLinkExpansionPreference(enabled=value if value is not None else False)
    )


@router.post("/{guild_id}/message_link_expand_preference", response_model=PlainAPIResponse)
async def update_guild_message_link_expand_pref(guild_id: int, data: MessageLinkExpansionPreference,
                                                _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        enabled = data.enabled
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
    return PlainAPIResponse(
        message="Updated guild data."
    )
