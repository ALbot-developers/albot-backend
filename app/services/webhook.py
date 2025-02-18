import json
from datetime import datetime

import asyncpg.connection
import stripe

from app import constants
from app.core.error import CustomHTTPException
from app.db.connection import get_connection_pool
from app.services import subscriptions

PRICE_IDS = {
    'monthly1': constants.MONTHLY1_PRICE_ID,
    'monthly2': constants.MONTHLY2_PRICE_ID,
    'yearly1': constants.YEARLY1_PRICE_ID,
    'yearly2': constants.YEARLY2_PRICE_ID
}


async def is_event_duplicated(event: stripe.Event):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if await conn.fetchrow("SELECT * FROM stripe_webhook_log WHERE event_id = $1", event.stripe_id):
            return True
        else:
            await conn.execute("""
            INSERT INTO stripe_webhook_log (event_id, event_type, obj_id) 
            VALUES ($1, $2, $3)
            """, event.stripe_id, event.type, event.data['object']['id'])
            return False


async def delete_subscription(subscription_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        subscription = await subscriptions.get(subscription_id)
        if subscription is None:
            raise CustomHTTPException(404, "Subscription not found")
        guild_id: int | None = subscription.guild_id
        if guild_id is not None:
            # registered_guild_table.delete(guild_id=guild_id)
            characters_limit = dict(wavenet=5000, standard=10000)
            # 使える文字数をリセット
            await conn.execute(
                "UPDATE word_count SET limit_word_count = $1 WHERE guild_id = $2",
                json.dumps(characters_limit), guild_id
            )
            # カスタム音声を無効に
            await conn.execute(
                "UPDATE settings_data SET custom_voice = null WHERE guild_id = $1",
                guild_id
            )
        # DBからサブスクを削除
        await conn.execute(
            "DELETE FROM subscriptions WHERE sub_id = $1",
            subscription_id
        )


async def update_subscription(subscription_id: str, price_id: str):
    subscription = await subscriptions.get(subscription_id)
    guild_id = subscription.guild_id if subscription else None
    # サブスクの種類変更に対応。
    _ = [k for k, v in PRICE_IDS.items() if v == price_id]
    new_plan = _[0] if _ else subscription.plan
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute("""
                            INSERT INTO subscriptions (sub_id, plan, last_updated) 
                            VALUES ($1, $2, $3)
                            ON CONFLICT (sub_id) DO UPDATE SET plan = excluded.plan, last_updated = excluded.last_updated
                        """, subscription_id, new_plan, datetime.now())
        if guild_id is not None:
            if "1" in new_plan:
                character_limit = {'wavenet': 20000, 'standard': 40000}
            elif "2" in new_plan:
                character_limit = {'wavenet': 100000, 'standard': 200000}
            else:
                raise ValueError("Invalid plan.")
            if subscription.sub_start != datetime.today():
                await conn.execute(
                    """
                    INSERT INTO word_count (guild_id, subscription, wavenet_count_now, standard_count_now, limit_word_count, is_overwritten)
                    VALUES ($1, $2, 0, 0, $3, true)
                    ON CONFLICT (guild_id) DO UPDATE SET 
                    subscription=excluded.subscription, 
                    wavenet_count_now=0, 
                    standard_count_now=0, 
                    limit_word_count=excluded.limit_word_count, 
                    is_overwritten=excluded.is_overwritten
                    """, guild_id, new_plan, json.dumps(character_limit)
                )


async def handle_checkout_completed(event: stripe.Event):
    sub_id = event.data['object']['subscription']
    metadata = event.data['object']["metadata"]
    if "discord_id" not in metadata:
        # donation
        return
    user_id: str = metadata["discord_id"]
    plan = metadata['plan']
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        await conn.execute("""
                        INSERT INTO subscriptions (sub_id, plan, user_id)
                        VALUES ($1, $2, $3) ON CONFLICT (sub_id) DO UPDATE set user_id = excluded.user_id
                    """, sub_id, plan, int(user_id))
        stripe.Subscription.modify(
            sub_id,
            metadata={"user_id": user_id}
        )
