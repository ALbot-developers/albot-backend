import json

import asyncpg
from fastapi import APIRouter, Security

from auth import verify_token
from db_connection import connection_pool

router = APIRouter()


@router.get("/{guild_id}/dict")
async def get_guild_dict(guild_id: int, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchval('SELECT dict FROM dict_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Fetched guild data.",
        "data": json.loads(row)
    }


@router.put("/{guild_id}/dict")
async def replace_guild_dict(guild_id: int, data: dict, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        await conn.execute('UPDATE dict_data SET dict = $1 WHERE guild_id = $2', json.dumps(data), guild_id)
    return {
        "message": "Updated guild data."
    }


@router.delete("/{guild_id}/dict")
async def delete_guild_dict(guild_id: int, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを削除
        await conn.execute('DELETE FROM dict_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Deleted guild data."
    }
