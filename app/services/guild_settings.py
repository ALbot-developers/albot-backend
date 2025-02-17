import asyncpg
from fastapi import HTTPException

from app.db.connection import get_connection_pool
from app.models.settings import GuildSettings, PremiumSettings
from app.models.subscription import Subscription
from app.schemas.guild_settings import GuildSettingsUpdate


async def get(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # guild_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM settings_data WHERE guild_id = $1', guild_id)
        # convert the row to a dictionary
        if row is None:
            return await get_default()
        return GuildSettings.from_dict(dict(row))


async def get_default() -> GuildSettings:
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
    return GuildSettings.from_dict(default_settings)


async def update(guild_id: int, settings: GuildSettingsUpdate, subscription: Subscription | None):
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
        if 'character_limit' in attributes:
            # replace to word_limit
            # todo: DBのカラム名をcharacter_limitに変更する
            attributes['word_limit'] = attributes.pop('character_limit')
        query = (
            f"INSERT INTO settings_data (guild_id, {', '.join(attributes.keys())}) "
            f"VALUES ({guild_id}, {', '.join([f'${i + 1}' for i in range(len(attributes))])}) "
            f"ON CONFLICT (guild_id) DO UPDATE SET "
            f"{', '.join([f'{k} = EXCLUDED.{k}' for k in attributes.keys()])}"
        )
        # execute the query with the values
        await conn.execute(query, *attributes.values())


async def delete(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'DELETE FROM settings_data WHERE guild_id = $1;', guild_id
        )
        await conn.execute(
            "INSERT INTO settings_data (guild_id) VALUES ($1) ON CONFLICT DO NOTHING", guild_id
        )
