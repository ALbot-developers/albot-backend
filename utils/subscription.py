import asyncpg
import stripe

from utils.db_connection import get_connection_pool

QUOTAS = {
    1: {'wavenet': 20000, 'standard': 40000},
    2: {'wavenet': 80000, 'standard': 160000}
}


async def cancel_subscription(sub_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE sub_id = $1', sub_id)
        if row is None:
            return False
    # noinspection PyTypeChecker
    stripe.Subscription.delete(sub_id)
    return True


async def activate_subscription(sub_id: str, guild_id: int):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow('SELECT * FROM subscriptions WHERE sub_id = $1', sub_id)
        if row is None or row["guild_id"]:
            return False
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
            guild_id, quota, plan)
        # set metadata
        stripe.Subscription.modify(
            sub_id,
            metadata={"user_id": row['user_id'], "guild_id": str(guild_id)},
        )
    return True
