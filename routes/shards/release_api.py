import asyncpg
from fastapi import APIRouter, Security

from utils.auth import verify_token
from utils.db_connection import get_connection_pool

router = APIRouter()


@router.post("/{shard_id}/release")
async def release_shard(shard_id: int, _auth=Security(lambda: verify_token("bearer"))):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # is_assignedをfalseに更新
        await conn.execute('UPDATE shard_data SET is_assigned = false WHERE shard_id = $1', shard_id)
    return {"message": "Shard released."}
