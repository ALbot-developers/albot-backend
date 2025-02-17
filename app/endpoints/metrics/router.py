import asyncpg
from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.db.connection import get_connection_pool

router = APIRouter()


@router.get("")
async def get_metrics(_auth=Security(verify_all_tokens)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetchrow(
            "SELECT SUM(connected_num) as connected, SUM(guilds_num) as guilds FROM shard_data")
    return {
        "message": "Fetched metrics.",
        "data": {
            "metrics": {
                "connected": res["connected"],
                "guilds": res["guilds"]
            }
        }
    }
