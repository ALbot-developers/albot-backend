import asyncpg
from fastapi import APIRouter, Security, HTTPException, Depends

from models.database import SettingsData, PremiumSettings
from models.subscription import Subscription
from utils.auth import verify_all_tokens
from utils.db_connection import get_connection_pool
from utils.dependencies import get_subscription

router = APIRouter()


async def get_default_settings() -> SettingsData:
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
    return SettingsData.from_dict(default_settings)


async def get_guild_settings(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM settings_data WHERE guild_id = $1', guild_id)
        # convert the row to a dictionary
        if row is None:
            return await get_default_settings()
        return SettingsData.from_dict(dict(row))


@router.get("/{guild_id}/settings")
async def get_guild_settings_api(guild_id: int, subscription: Subscription = Depends(get_subscription),
                                 _auth=Security(verify_all_tokens)):
    settings = await get_guild_settings(guild_id)
    if subscription is None:
        default_settings = await get_default_settings()
        for key in PremiumSettings.__annotations__.keys():
            if key not in settings.__dict__:
                continue
            setattr(settings, key, getattr(default_settings, key))
    return {
        "message": "Fetched guild data.",
        "data": {
            "settings": settings
        }
    }


@router.post("/{guild_id}/settings")
async def update_guild_settings(guild_id: int, settings: SettingsData,
                                subscription: Subscription = Depends(get_subscription),
                                _auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # get all attributes with values
        attributes = {k: (None if v == "" else v) for k, v in settings.__dict__.items() if v is not None}
        if not attributes:
            raise HTTPException(status_code=400, detail="No settings data provided.")
        # if subscription is None and PremiumSettings in attributes, return an error
        if subscription is None:
            if any(k in attributes for k in PremiumSettings.__annotations__.keys()):
                raise HTTPException(status_code=403, detail="Requires premium subscription.")
        # noinspection DuplicatedCode
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
        await conn.execute(
            '''
            DELETE FROM settings_data WHERE guild_id = $1;
            INSERT INTO settings_data (guild_id) VALUES ($1);
            ''',
            guild_id
        )
    return {
        "message": "Deleted guild data."
    }
