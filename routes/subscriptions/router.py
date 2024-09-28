from fastapi import APIRouter, Security, Response

from type_specifications.api_payload import ActivateSubscriptionAPIPayload, RenewSubscriptionAPIPayload
from utils.auth import verify_token
from utils.subscription import activate_subscription, cancel_subscription, renew_subscription

router = APIRouter()


@router.get("/{sub_id}/activate")
async def activate_subscriptions_api(
        sub_id: str,
        response: Response,
        payload: ActivateSubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await activate_subscription(sub_id, payload.guild_id)
    response.status_code = status
    return {
        "message": message
    }


@router.get("/{sub_id}/cancel")
async def cancel_subscriptions_api(
        sub_id: str,
        response: Response,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await cancel_subscription(sub_id)
    response.status_code = status
    return {
        "message": message
    }


@router.get("/{sub_id}/renew")
async def renew_subscriptions_api(
        sub_id: str,
        response: Response,
        payload: RenewSubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await renew_subscription(sub_id, payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }
