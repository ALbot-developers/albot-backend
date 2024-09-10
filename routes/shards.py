import asyncpg
from fastapi import APIRouter, Security

import envs
from auth import verify_token
from db_connection import connection_pool

router = APIRouter()


@router.get("/assign")
async def assign_shard(_auth=Security(lambda: verify_token("bearer"))):
    async with connection_pool.acquire() as conn:
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


@router.get("/{shard_id}/release")
async def release_shard(shard_id: int, _auth=Security(lambda: verify_token("bearer"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # is_assignedをfalseに更新
        await conn.execute('UPDATE shard_data SET is_assigned = false WHERE shard_id = $1', shard_id)
    return {"message": "Shard released."}


@router.get("/{shard_id}/connection_commands")
async def get_connection_commands(shard_id: int, _auth=Security(lambda: verify_token("bearer"))):
    async with connection_pool.acquire() as conn:
        conn: asyncpg.connection.Connection
        # shard_idのデータを取得
        rows = await conn.fetch(
            'SELECT guild_id, command FROM connect_command WHERE (guild_id >> 22) % $1 = $2',
            envs.SHARD_COUNT, shard_id
        )
    data = {}
    for row in rows:
        data[row["guild_id"]] = row["command"]
    return {
        "message": "Fetched connection commands.",
        "data": data
    }
