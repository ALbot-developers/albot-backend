import stripe
from fastapi import APIRouter, Request

import app.services.webhook
from app.constants import STRIPE_WEBHOOK_SECRET
from app.core.error import CustomHTTPException
from app.schemas.api_response import PlainAPIResponse
from app.services import webhook

router = APIRouter()


def construct_event(payload: bytes, received_sig: str):
    try:
        return stripe.Webhook.construct_event(
            payload.decode('utf-8'), received_sig, STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        raise CustomHTTPException(400, "Bad payload")
    except stripe.error.SignatureVerificationError:
        raise CustomHTTPException(400, "Bad signature")


@router.post("", response_model=PlainAPIResponse)
async def stripe_webhook(request: Request):
    payload = await request.body()
    received_sig = request.headers.get("Stripe-Signature")
    event = construct_event(payload, received_sig)
    if await app.services.webhook.is_event_duplicated(event):
        # 再送を防ぐために2xxに
        raise CustomHTTPException(202, "Duplicate event.")
    if event.type.startswith('customer.subscription'):
        sub_id = event.data['object']['id']
        if event.type == 'customer.subscription.deleted':
            await webhook.delete_subscription(sub_id)
            return PlainAPIResponse(message="subscription deleted.")
        elif event.type == 'customer.subscription.updated':
            price_id = event.data['object']['items']['data'][0]["price"]['id']
            await webhook.update_subscription(sub_id, price_id)
            return PlainAPIResponse(message="subscription updated.")
        else:
            raise CustomHTTPException(422, "Unexpected event type.")
    elif event.type == 'checkout.session.completed':
        await webhook.handle_checkout_completed(event)
        return PlainAPIResponse(message="subscription created.")
    else:
        raise CustomHTTPException(422, "Unexpected event type.")
