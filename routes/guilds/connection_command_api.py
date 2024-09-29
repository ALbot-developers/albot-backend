from typing import Dict, Literal

import asyncpg
from fastapi import APIRouter, Security, Response

from utils.auth import verify_token
from utils.db_connection import get_connection_pool

router = APIRouter()

EXISTING_COMMANDS = ("t.help", "t.id", "t.status", "t.expand", "t.act", "t.dict", "t.view", "t.save", "t.dc", "t.con")


@router.get("/{guild_id}/connection_command")
async def get_guild_connection_command(
        guild_id: int,
        _auth=Security(lambda: verify_token("jwt"))
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT command FROM connect_command WHERE guild_id = $1', guild_id)
    return {
        "message": "Fetched connection command.",
        "data": {
            "command": row["command"]
        }
    }


@router.put("/{guild_id}/connection_command")
async def update_guild_connection_command(
        response: Response,
        guild_id: int,
        data: Dict[Literal["command"], str],
        _auth=Security(lambda: verify_token("jwt"))
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        command = data["command"]
        for command_ in EXISTING_COMMANDS:
            if command_.startswith(command):
                response.status_code = 400
                return {
                    "message": "Command already exists."
                }
        await conn.execute('UPDATE connect_command SET command = $1 WHERE guild_id = $2', command, guild_id)
    return {
        "message": "Updated connection command."
    }
