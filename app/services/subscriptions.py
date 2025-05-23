import calendar
import json
import math
from datetime import datetime
from typing import Literal, List

import asyncpg
import sentry_sdk
import stripe

from app.constants import PRICE_IDS
from app.db.connection import get_connection_pool
from app.models.subscription import Subscription

QUOTAS = {
    1: {'wavenet': 20000, 'standard': 40000},
    2: {'wavenet': 80000, 'standard': 160000}
}


async def _does_subscription_exist(user_id: int, sub_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow("SELECT * FROM subscriptions WHERE user_id=$1 and sub_id=$2", user_id, sub_id)
        return row is not None


def _create_remaining_payment(subscription, old_plan: str):
    # 未使用の一ヶ月分を算出
    full_amount = 200 if "1" in old_plan else 400
    days_in_this_month = calendar.monthrange(datetime.now().year, datetime.now().month)[1]
    remaining_amount = full_amount * ((days_in_this_month - datetime.now().day) / days_in_this_month)
    remaining_amount = math.ceil(remaining_amount)
    stripe.PaymentIntent.create(
        amount=remaining_amount if remaining_amount >= 50 else 50,
        currency='jpy',
        customer=subscription["customer"],
        payment_method_types=['card'],
        description="年額プランの更新により、未使用の一ヶ月分を決済しました。",
        payment_method=subscription["default_payment_method"],
        confirm=True,
        off_session=True,
    )


async def list_by_user(user_id: int) -> List[Subscription]:
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch("SELECT * FROM subscriptions WHERE user_id = $1", user_id)
        subscriptions = []
        for row in res:
            subscription = Subscription.from_dict(dict(row))
            subscriptions.append(subscription)
    return subscriptions


async def list_by_guild(guild_id: int) -> List[Subscription]:
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch("SELECT * FROM subscriptions WHERE guild_id = $1", guild_id)
        subscriptions = []
        for row in res:
            subscription = Subscription.from_dict(dict(row))
            subscriptions.append(subscription)
    return subscriptions


async def get(sub_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow("SELECT * FROM subscriptions WHERE sub_id = $1", sub_id)
    return Subscription.from_dict(dict(row)) if row else None

async def cancel(sub_id: str, user_id: int) -> tuple[int, str]:
    if not await _does_subscription_exist(user_id, sub_id):
        return 400, "Subscription not found."
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE sub_id = $1', sub_id)
        if row is None:
            return 400, "Subscription not found."
    # noinspection PyTypeChecker
    stripe.Subscription.delete(sub_id)
    return 200, "Successfully canceled."


# todo: HTTPExceptionを吐くなど、リファクタリング
async def activate(sub_id: str, user_id: int, guild_id: int) -> tuple[int, str]:
    if not await _does_subscription_exist(user_id, sub_id):
        return 400, "Subscription not found."
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE sub_id = $1', sub_id)
        if row is None or row["guild_id"]:
            return 400, "Subscription not found."
        # update
        plan = row["plan"]
        await conn.execute('UPDATE subscriptions SET guild_id = $1 WHERE sub_id = $2', guild_id, sub_id)
        # get quota
        if "1" in plan:
            quota = QUOTAS[1]
        else:
            quota = QUOTAS[2]
        # upsert
        await conn.execute(
            '''
        INSERT INTO word_count (guild_id, limit_word_count, subscription, created_at) VALUES ($1, $2, $3, NOW())
        ON CONFLICT (guild_id) DO UPDATE SET limit_word_count = $2, subscription = $3, created_at = NOW()
        ''',
            guild_id, json.dumps(quota), plan)
        # set metadata
        stripe.Subscription.modify(
            sub_id,
            metadata={"user_id": row['user_id'], "guild_id": str(guild_id)},
        )
    return 200, "Successfully activated."


async def renew(sub_id: str, user_id: int, new_plan: str) -> tuple[int, str]:
    if not await _does_subscription_exist(user_id, sub_id):
        return 400, "Subscription not found."
    new_price_id = PRICE_IDS[new_plan]
    old_sub = stripe.Subscription.retrieve(sub_id)
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        old_plan: str = await conn.fetchval('SELECT plan FROM subscriptions WHERE sub_id = $1', sub_id)
    proration_behavior: Literal["create_prorations", "none"] = "none"
    # 変更前のプランが年額の場合
    # todo: 一時的なエラーハンドリング。ちゃんと直す
    if "yearly" in old_plan:
        proration_behavior = "create_prorations"
        try:
            _create_remaining_payment(old_sub, old_plan)
        except stripe.error.StripeError as e:
            sentry_sdk.capture_exception(e)
            pass
    # サブスクのダウングレード・アップグレード
    if old_sub["items"]["data"][0]["price"]["id"] != new_price_id:
        stripe.Subscription.modify(
            sub_id,
            cancel_at_period_end=False,
            proration_behavior=proration_behavior,
            items=[{
                'id': old_sub['items']['data'][0].id,
                'price': new_price_id,
            }]
        )
    # 同じサブスクを更新
    else:
        stripe.Subscription.modify(sub_id,
                                   billing_cycle_anchor='now',
                                   proration_behavior=proration_behavior,
                                   )
    return 200, "Successfully renewed."
