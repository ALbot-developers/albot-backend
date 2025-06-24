import stripe

from app import constants


def create_checkout_session(user_id: int, plan: str):
    success_url = "https://mypage.albot.info/subscribed"
    cancel_url = f"https://albot.info/#pricing"
    price_id = constants.PRICE_IDS[plan]
    stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        allow_promotion_codes=True,
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        success_url=success_url,
        cancel_url=cancel_url,
        mode='subscription',
        metadata={
            "discord_id": user_id,
            "plan": plan
        }
    )
    return stripe_session
