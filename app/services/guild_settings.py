import asyncpg

from app.db.connection import get_connection_pool
from app.models.settings import GuildSettings


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
