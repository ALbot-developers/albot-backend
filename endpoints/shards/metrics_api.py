from dataclasses import dataclass
from typing import Optional

import asyncpg
from fastapi import APIRouter, Security

from core.auth import verify_bearer_token
from db.connection import get_connection_pool

router = APIRouter()


@dataclass
class ShardMetricsPostPayload:
    connected: Optional[int] = None
    guilds: Optional[int] = None


@router.post("/{shard_id}/metrics")
async def post_metrics(
        shard_id: int,
        payload: ShardMetricsPostPayload,
        _auth=Security(verify_bearer_token)
):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if payload.connected:
            await conn.execute(
                'UPDATE shard_data SET connected_num = $1 WHERE shard_id = $2',
                payload.connected, shard_id
            )
        if payload.guilds:
            await conn.execute(
                'UPDATE shard_data SET guilds_num = $1 WHERE shard_id = $2',
                payload.guilds, shard_id
            )

    return {
        "message": "Updated metrics."
    }
