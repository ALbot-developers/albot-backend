import asyncpg

from app.db.connection import get_connection_pool
from app.models.quick_report import QuickReport


async def get_by_id(report_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetchrow(
            "SELECT * FROM quick_reports WHERE id = $1", report_id
        )
    return QuickReport.model_validate(dict(res))


async def get_by_guild(guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch(
            "SELECT * FROM quick_reports WHERE guild_id = $1", guild_id
        )
    return [QuickReport.model_validate(dict(i)) for i in res]


async def create(guild_id: int, category: str, description: str):
    """
    Creates a new quick report entry in the database.

    Args:
        guild_id (int): The ID of the Discord guild
        category (str): The category of the quick report
        description (str): The description of the quick report

    Returns:
        The ID of the newly created quick report
    """
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.execute(
            "INSERT INTO quick_reports (guild_id, category, description) VALUES ($1, $2, $3) RETURNING id",
            guild_id, category, description
        )
    return res
