import asyncpg
from fastapi import APIRouter, Security

from auth import verify_token
from db_connection import connection_pool
from type_specifications.database import SettingsData

router = APIRouter()


@router.get("/{guild_id}/settings")
async def get_guild_settings(guild_id: int, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchval('SELECT * FROM settings_data WHERE guild_id = $1', guild_id)
        # convert the row to a dictionary
        settings_data = SettingsData.from_dict(dict(row))
    return {
        "message": "Fetched guild data.",
        "data": settings_data.to_json()
    }


@router.post("/{guild_id}/settings")
async def update_guild_settings(guild_id: int, data: dict, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを更新
        data = SettingsData.from_dict(data)
        # get all attributes with values
        attributes = {k: v for k, v in data.__dict__.items() if v is not None}
        # create a query string with placeholders for the attributes
        query = (
            f"UPDATE settings_data"
            f" SET {', '.join([f'{k} = ${i + 1}' for i, (k, v) in enumerate(attributes.items())])}"
            f" WHERE guild_id = {guild_id}"
        )
        # execute the query with the values
        await conn.execute(query, *attributes.values())
    return {
        "message": "Updated guild data."
    }


@router.delete("/{guild_id}/settings")
async def delete_guild_settings(guild_id: int, _auth=Security(lambda: verify_token("all"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを削除
        await conn.execute('DELETE FROM settings_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Deleted guild data."
    }
