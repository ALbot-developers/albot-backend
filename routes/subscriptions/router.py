from fastapi import APIRouter, Security, Response

from type_specifications.api_payload import SubscriptionAPIPayload
from utils.auth import verify_token
from utils.subscription import activate_subscription, cancel_subscription

router = APIRouter()


@router.get("/{sub_id}/activate")
async def activate_subscriptions_api(
        sub_id: str,
        response: Response,
        payload: SubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    res = await activate_subscription(sub_id, payload.guild_id)
    if not res:
        response.status_code = 400
        return {
            "message": "Failed to activate subscription."
        }
    return {
        "message": "Successfully activated."
    }


@router.get("/{sub_id}/cancel")
async def cancel_subscriptions_api(
        sub_id: str,
        response: Response,
        payload: SubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    res = await cancel_subscription(sub_id)
    if not res:
        response.status_code = 400
        return {
            "message": "Failed to cancel subscription."
        }
