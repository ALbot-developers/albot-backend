import asyncpg
from fastapi import APIRouter, Security, Response

from app.core.auth import verify_all_tokens
from app.db.connection import get_connection_pool
from app.schemas.api_response import ConnectionCommandAPIResponse, PlainAPIResponse
from app.schemas.connection_command import ConnectionCommand

router = APIRouter()

EXISTING_COMMANDS = ("t.help", "t.id", "t.status", "t.expand", "t.act", "t.dict", "t.view", "t.save", "t.dc")


@router.get("/{guild_id}/connection_command", response_model=ConnectionCommandAPIResponse)
async def get_guild_connection_command(
        guild_id: int,
        _auth=Security(verify_all_tokens)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        command = await conn.fetchval('SELECT command FROM connect_command WHERE guild_id = $1', guild_id)
    return ConnectionCommandAPIResponse(
        message="Fetched connection command.",
        data=ConnectionCommand(command=command if command else "t.con")
    )


@router.put("/{guild_id}/connection_command", response_model=PlainAPIResponse)
async def update_guild_connection_command(
        response: Response,
        guild_id: int,
        payload: ConnectionCommand,
        _auth=Security(verify_all_tokens)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        for _ in EXISTING_COMMANDS:
            if _.startswith(payload.command):
                response.status_code = 400
                return {
                    "message": "Command already exists."
                }
        # upsert
        await conn.execute(
            'INSERT INTO connect_command (guild_id, command) VALUES ($1, $2) ON CONFLICT (guild_id) DO UPDATE SET command = $2',
            guild_id, payload.command)
    return PlainAPIResponse(
        message="Updated connection command."
    )
