import asyncpg
from fastapi import APIRouter, Security

from type_specifications.database import SettingsData
from utils.auth import verify_all_tokens
from utils.db_connection import get_connection_pool

router = APIRouter()


async def get_default_settings():
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # settings_dataのデフォルト値を取得
        # noinspection SqlResolve
        rows = await conn.fetch(
            "SELECT column_name, column_default, data_type "
            "FROM INFORMATION_SCHEMA.COLUMNS WHERE table_name = 'settings_data';"
        )

    def fix_value_type(value, value_type):
        if value_type in ['int', 'tinyint', 'smallint', 'mediumint', 'bigint', 'integer']:
            return int(value)
        elif value_type in ['float', 'double', 'decimal', 'double precision']:
            return float(value)
        elif value_type == 'boolean':
            if value == "true":
                return True
            elif value == "false":
                return False
        return value

    default_settings = {}
    for row in rows:
        if row["column_name"] == "guild_id":
            continue
        column_default = row["column_default"]
        if isinstance(column_default, str):
            if "::text" in column_default:
                column_default = column_default.replace("'::text", "")
                column_default = column_default.replace("'", "")
        column_default = fix_value_type(column_default, row["data_type"])
        default_settings[row["column_name"]] = column_default
    return default_settings


async def get_guild_settings(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM settings_data WHERE guild_id = $1', guild_id)
        # convert the row to a dictionary
        if row is None:
            return SettingsData.from_dict(await get_default_settings())
        return SettingsData.from_dict(dict(row))


@router.get("/{guild_id}/settings")
async def get_guild_settings_api(guild_id: int, _auth=Security(verify_all_tokens)):
    settings = await get_guild_settings(guild_id)
    return {
        "message": "Fetched guild data.",
        "data": {
            "settings": settings
        }
    }


@router.post("/{guild_id}/settings")
async def update_guild_settings(guild_id: int, data: dict, _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # convert the data to a SettingsData object (to validate the data)
        settings_data = SettingsData.from_dict(data)
        # get all attributes with values
        attributes = {k: v for k, v in settings_data.__dict__.items() if v is not None}
        # create a query string with placeholders for the attributes
        query = (
            f"INSERT INTO settings_data (guild_id, {', '.join(attributes.keys())}) "
            f"VALUES ({guild_id}, {', '.join([f'${i + 1}' for i in range(len(attributes))])}) "
            f"ON CONFLICT (guild_id) DO UPDATE SET "
            f"{', '.join([f'{k} = EXCLUDED.{k}' for k in attributes.keys()])}"
        )
        # execute the query with the values
        await conn.execute(query, *attributes.values())
    return {
        "message": "Updated guild data."
    }


@router.delete("/{guild_id}/settings")
async def delete_guild_settings(guild_id: int, _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを削除
        await conn.execute('DELETE FROM settings_data WHERE guild_id = $1', guild_id)
    return {
        "message": "Deleted guild data."
    }
