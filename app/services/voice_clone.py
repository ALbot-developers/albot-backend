import base64

import aiohttp

from app import constants
from app.db.connection import get_connection_pool

CLONE_API_URL = "https://dashscope-intl.aliyuncs.com/api/v1/services/audio/tts/customization"
CLONE_MODEL = "qwen-voice-enrollment"
DEFAULT_TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15"


async def create_voice(audio_data: bytes, mime_type: str) -> str:
    base64_str = base64.b64encode(audio_data).decode()
    data_uri = f"data:{mime_type};base64,{base64_str}"

    payload = {
        "model": CLONE_MODEL,
        "input": {
            "action": "create",
            "target_model": DEFAULT_TARGET_MODEL,
            "audio": {"data": data_uri}
        }
    }
    headers = {
        "Authorization": f"Bearer {constants.DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(CLONE_API_URL, json=payload, headers=headers) as resp:
            if resp.status != 200:
                text = await resp.text()
                raise RuntimeError(f"Failed to create voice: {resp.status}, {text}")
            body = await resp.json()

    try:
        return body["output"]["voice"]
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Failed to parse voice response: {e}")


async def save_cloned_voice(guild_id: int, user_id: int, voice: str):
    async with get_connection_pool().acquire() as conn:
        await conn.execute(
            "INSERT INTO cloned_voices (guild_id, user_id, voice) VALUES ($1, $2, $3) "
            "ON CONFLICT (voice) DO UPDATE SET guild_id = $1, user_id = $2",
            guild_id, user_id, voice
        )


async def list_by_guild(guild_id: int) -> list[dict]:
    async with get_connection_pool().acquire() as conn:
        rows = await conn.fetch(
            "SELECT guild_id, user_id, voice FROM cloned_voices WHERE guild_id = $1",
            guild_id
        )
    return [dict(row) for row in rows]


async def list_by_user(user_id: int) -> list[dict]:
    async with get_connection_pool().acquire() as conn:
        rows = await conn.fetch(
            "SELECT guild_id, user_id, voice FROM cloned_voices WHERE user_id = $1",
            user_id
        )
    return [dict(row) for row in rows]
