from typing import Literal, Optional

import asyncpg
from fastapi import APIRouter, Security

from routes.shards import release_api, assign_api, connection_commands_api, metrics_api
from utils.auth import verify_session
from utils.db_connection import get_connection_pool

router = APIRouter()
router.include_router(assign_api.router)
router.include_router(release_api.router)
router.include_router(connection_commands_api.router)
router.include_router(metrics_api.router)


# todo: 将来的には死活監視の情報を使用
@router.get("")
async def index(
        _auth=Security(verify_session),
        status: Optional[Literal["online", "offline", "all"]] = "all"
):
    if status == "all":
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data"
            )
    elif status == "online":
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data WHERE is_assigned is true"
            )
    else:
        async with get_connection_pool().acquire() as conn:
            conn: asyncpg.connection.Connection
            res = await conn.fetch(
                "SELECT shard_id FROM shard_data WHERE is_assigned is false"
            )
    shard_ids = [int(i[0]) for i in res]
    return {
        "message": "Fetched shard IDs.",
        "data": {
            "ids": shard_ids
        }
    }
