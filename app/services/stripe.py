import stripe

from app import constants
from app.db.connection import get_connection_pool


async def create_checkout_session(user_id: int, plan: str):
    success_url = "https://mypage.albot.info/subscribed"
    cancel_url = f"https://albot.info/#pricing"
    price_id = constants.PRICE_IDS[plan]

    # DBから既存の顧客IDを取得
    async with get_connection_pool().acquire() as conn:
        customer_id = await conn.fetchval("SELECT stripe_customer_id FROM users WHERE user_id = $1", user_id)

    params = {
        'payment_method_types': ['card'],
        'allow_promotion_codes': True,
        'line_items': [{
            'price': price_id,
            'quantity': 1,
        }],
        'success_url': success_url,
        'cancel_url': cancel_url,
        'mode': 'subscription',
        'metadata': {
            "discord_id": user_id,
            "plan": plan
        },
        'consent_collection': {
            'terms_of_service': 'required'
        }
    }

    if customer_id:
        # 既存顧客を指定
        params['customer'] = customer_id

    stripe_session = stripe.checkout.Session.create(**params)
    return stripe_session


async def create_customer_portal_session(user_id: int):
    # DBから既存の顧客IDを取得
    async with get_connection_pool().acquire() as conn:
        customer_id = await conn.fetchval("SELECT stripe_customer_id FROM users WHERE user_id = $1", user_id)

    if not customer_id:
        return None

    portal_session = stripe.billing_portal.Session.create(
        customer=customer_id,
        return_url="https://mypage.albot.info/",
    )
    return portal_session
