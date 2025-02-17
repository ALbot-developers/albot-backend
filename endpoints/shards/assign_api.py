import asyncpg
from fastapi import APIRouter, Security, HTTPException

import constants
from utils.auth import verify_bearer_token
from utils.db_connection import get_connection_pool

router = APIRouter()


@router.get("/assign")
async def assign_shard(_auth=Security(verify_bearer_token)):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # SQLクエリを実行
        # is_assignedがfalseのshard_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM shard_data WHERE is_assigned = false LIMIT 1')
        total_shards = await conn.fetchval('SELECT COUNT(*) FROM shard_data')
        if row is None:
            raise HTTPException(status_code=400, detail="No available shards.")
        # shard_idを取得
        shard_id = row['shard_id']
        tts_key = row["tts_key"]
        heartbeat_token = row["shardd_token"]
        # is_assignedをtrueに更新
        await conn.execute('UPDATE shard_data SET is_assigned = true WHERE shard_id = $1', shard_id)
    return {
        "message": "Shard assigned.",
        "data": {
            "shard_count": int(total_shards),
            "shard_id": shard_id,
            "discord_token": constants.BOT_DISCORD_TOKEN,
            "sentry_dsn": constants.BOT_SENTRY_DSN,
            "tts_key": tts_key,
            "heartbeat_token": heartbeat_token
        }
    }
