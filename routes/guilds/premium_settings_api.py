import asyncpg
from fastapi import APIRouter, Security, Depends, HTTPException

from models.database import PremiumSettings
from models.subscription import Subscription
from utils.auth import verify_all_tokens
from utils.db_connection import get_connection_pool
from utils.dependencies import get_subscription

router = APIRouter()


@router.get("/{guild_id}/premium_settings")
async def get_premium_settings(guild_id: int, _auth=Security(verify_all_tokens),
                               subscription: Subscription = Depends(get_subscription)):
    if not subscription:
        raise HTTPException(status_code=403, detail="Requires premium subscription.")
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow(
            'SELECT guild_id, read_name_on_join, read_name_on_leave, custom_voice FROM settings_data WHERE guild_id = $1',
            guild_id)
        if row:
            data = PremiumSettings(
                guild_id=guild_id,
                read_name_on_join=row['read_name_on_join'],
                read_name_on_leave=row['read_name_on_leave'],
                custom_voice=row['custom_voice'],
                sub_id=subscription.sub_id
            )
        else:
            data = PremiumSettings(
                guild_id=guild_id,
                read_name_on_join=False,
                read_name_on_leave=False,
                custom_voice=None,
                sub_id=subscription.sub_id
            )
    return {
        "message": "Fetched guild data.",
        "data": {
            "premium_settings": data
        }
    }


@router.post("/{guild_id}/premium_settings")
async def update_premium_settings(guild_id: int, payload: PremiumSettings, _auth=Security(verify_all_tokens),
                                  subscription: Subscription = Depends(get_subscription)):
    if not subscription:
        raise HTTPException(status_code=403, detail="Requires premium subscription.")
    attributes = {k: (None if v == "" else v) for k, v in payload.__dict__.items() if v is not None}
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        # noinspection DuplicatedCode
        query = (
            f"INSERT INTO settings_data (guild_id, {', '.join(attributes.keys())}) "
            f"VALUES ({guild_id}, {', '.join([f'${i + 1}' for i in range(len(attributes))])}) "
            f"ON CONFLICT (guild_id) DO UPDATE SET "
            f"{', '.join([f'{k} = EXCLUDED.{k}' for k in attributes.keys()])}"
        )
        await conn.execute(query, *attributes.values())
    return {
        "message": "Updated guild data."
    }
