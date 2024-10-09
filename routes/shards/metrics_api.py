from dataclasses import dataclass

import asyncpg
from fastapi import APIRouter, Security

from utils.auth import verify_bearer_token
from utils.db_connection import get_connection_pool

router = APIRouter()


@dataclass
class ShardMetricsPostPayload:
    connected: int
    guilds: int


@router.post("/{shard_id}/metrics")
async def post_metrics(
        shard_id: int,
        payload: ShardMetricsPostPayload,
        _auth=Security(verify_bearer_token)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute(
            'UPDATE shard_data SET connected_num = $1, guilds_num = $2 WHERE shard_id = $3',
            payload.connected, payload.guilds, shard_id
        )
    return {
        "message": "Updated metrics."
    }
