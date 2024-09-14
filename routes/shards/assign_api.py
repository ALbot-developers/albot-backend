import asyncpg
from fastapi import APIRouter, Security

from auth import verify_token
from db_connection import get_connection_pool

router = APIRouter()


@router.get("/assign")
async def assign_shard(_auth=Security(lambda: verify_token("bearer"))):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # SQLクエリを実行
        # is_assignedがfalseのshard_idのデータを取得
        row = await conn.fetchrow('SELECT * FROM shard_data WHERE is_assigned = false LIMIT 1')
        # shard_idを取得
        shard_id = row['shard_id']
        tts_key = row["tts_key"]
        heartbeat_token = row["shardd_token"]
        # is_assignedをtrueに更新
        await conn.execute('UPDATE shard_data SET is_assigned = true WHERE shard_id = $1', shard_id)
    return {
        "message": "Shard assigned.",
        "data": {
            "shard_id": shard_id,
            "discord_token": "bot_token",
            "sentry_dsn": "sentry_dsn",
            "tts_key": tts_key,
            "heartbeat_token": heartbeat_token
        }
    }
