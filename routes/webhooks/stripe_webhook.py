import json
from datetime import datetime

import asyncpg.connection
import stripe
from fastapi import APIRouter, Request, Response, HTTPException

from constants import STRIPE_WEBHOOK_SECRET, MONTHLY1_PRICE_ID, YEARLY1_PRICE_ID, MONTHLY2_PRICE_ID, YEARLY2_PRICE_ID
from utils.db_connection import get_connection_pool

router = APIRouter()

PRICE_IDS = {
    'monthly1': MONTHLY1_PRICE_ID,
    'monthly2': MONTHLY2_PRICE_ID,
    'yearly1': YEARLY1_PRICE_ID,
    'yearly2': YEARLY2_PRICE_ID
}


async def is_event_duplicated(event: stripe.Event, conn: asyncpg.connection.Connection):
    if await conn.fetchrow("SELECT * FROM stripe_webhook_log WHERE event_id = $1", event.stripe_id):
        return True
    else:
        await conn.execute("""
        INSERT INTO stripe_webhook_log (event_id, event_type, obj_id) 
        VALUES ($1, $2, $3)
        """, event.stripe_id, event.type, event.data['object']['id'])
        return False


async def construct_event(payload: bytes, received_sig: str):
    try:
        return stripe.Webhook.construct_event(
            payload.decode('utf-8'), received_sig, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise HTTPException(400, "Bad payload.")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(400, "Bad signature.")


@router.post("")
async def stripe_webhook(request: Request, response: Response):
    payload = await request.body()
    received_sig = request.headers.get("Stripe-Signature")
    event = await construct_event(payload, received_sig)
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        if await is_event_duplicated(event, conn):
            # 再送を防ぐために2xxに
            raise HTTPException(202, "Duplicated event.")

        if event.type.startswith('customer.subscription'):
            sub_id = event.data['object']['id']
            sub_entry = await conn.fetchrow("SELECT * FROM subscriptions WHERE sub_id = $1", sub_id)
            if event.type == 'customer.subscription.deleted':
                guild_id: int | None = sub_entry['guild_id']
                if guild_id is not None:
                    # registered_guild_table.delete(guild_id=guild_id)
                    # todo: 減らす
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
                    sub_id
                )
                return {"message": "subscription removed."}
            elif event.type == 'customer.subscription.updated':
                event_price_id = event.data['object']['items']['data'][0]["price"]['id']
                guild_id = sub_entry['guild_id'] if sub_entry else None
                # サブスクの種類変更に対応。
                _ = [k for k, v in PRICE_IDS.items() if v == event_price_id]
                new_plan = _[0] if _ else sub_entry["plan"]
                await conn.execute("""
                    INSERT INTO subscriptions (sub_id, plan, last_updated) 
                    VALUES ($1, $2, $3)
                    ON CONFLICT (sub_id) DO UPDATE SET plan = excluded.plan, last_updated = excluded.last_updated
                """, sub_id, new_plan, datetime.now())
                if guild_id is not None:
                    if "1" in new_plan:
                        character_limit = {'wavenet': 20000, 'standard': 40000}
                    elif "2" in new_plan:
                        character_limit = {'wavenet': 100000, 'standard': 200000}
                    else:
                        raise ValueError
                    if sub_entry['sub_start'] != datetime.today():
                        await conn.execute("""
                        INSERT INTO word_count (guild_id, subscription, wavenet_count_now, standard_count_now, limit_word_count, is_overwritten)
                        VALUES ($1, $2, 0, 0, $3, true)
                        ON CONFLICT (guild_id) DO UPDATE SET 
                        subscription=excluded.subscription, 
                        wavenet_count_now=0, 
                        standard_count_now=0, 
                        limit_word_count=excluded.limit_word_count, 
                        is_overwritten=excluded.is_overwritten
                        """, guild_id, new_plan, json.dumps(character_limit))
                return {"message": "subscription updated."}
        elif event.type == 'checkout.session.completed':
            sub_id = event.data['object']['subscription']
            metadata = event.data['object']["metadata"]
            if "discord_id" not in metadata:
                return {"message": "donation completed."}
            user_id: str = metadata["discord_id"]
            plan = metadata['plan']
            await conn.execute("""
                INSERT INTO subscriptions (sub_id, plan, user_id)
                VALUES ($1, $2, $3) ON CONFLICT (sub_id) DO NOTHING
            """, sub_id, plan, int(user_id))
            stripe.Subscription.modify(
                sub_id,
                metadata={"user_id": user_id}
            )
            return {"message": "subscription created."}
        else:
            return HTTPException(422, "Unexpected event type.")
