import asyncpg
from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.db.connection import get_connection_pool
from app.endpoints.guilds import dict_api, connection_command_api, subscriptions_api, settings_api, \
    connection_states_api, trusted_roles_api, character_usage_api, message_link_expand_pref_api

router = APIRouter()
router.include_router(dict_api.router)
router.include_router(settings_api.router)
router.include_router(character_usage_api.router)
router.include_router(trusted_roles_api.router)
router.include_router(connection_command_api.router)
router.include_router(connection_states_api.router)
router.include_router(message_link_expand_pref_api.router)
router.include_router(subscriptions_api.router)


@router.post("/{guild_id}")
async def create_guild_resources(
        guild_id: int,
        _auth=Security(verify_bearer_token)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'INSERT INTO settings_data (guild_id) VALUES ($1) ON CONFLICT DO NOTHING',
            guild_id
        )
        # await conn.execute(
        #     'INSERT INTO word_count (guild_id) VALUES ($1) ON CONFLICT DO NOTHING',
        #     guild_id
        # )
    return {
        "message": "Created guild resources."
    }


@router.delete("/{guild_id}")
async def delete_guild_resources(
        guild_id: int,
        _auth=Security(verify_bearer_token)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # word countは削除しない
        await conn.execute('DELETE FROM settings_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Deleted guild resources."
    }
