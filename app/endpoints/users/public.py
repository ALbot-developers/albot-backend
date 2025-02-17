from fastapi import APIRouter, Security, Response

from app.core.auth import verify_bearer_token
from app.models.api_payload import ActivateSubscriptionAPIPayload, RenewSubscriptionAPIPayload
from app.services.subscription import activate_subscription, cancel_subscription, renew_subscription, \
    list_user_subscriptions

router = APIRouter()


@router.get("/{user_id}/subscriptions")
async def list_subscriptions_api(
        user_id: int,
        _auth=Security(verify_bearer_token)
):
    subscriptions = await list_user_subscriptions(user_id)
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": subscriptions
        }
    }


@router.post("/{user_id}/subscriptions/{sub_id}/activate")
async def activate_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: ActivateSubscriptionAPIPayload,
        _auth=Security(verify_bearer_token)
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await activate_subscription(sub_id, user_id, payload.guild_id)
    response.status_code = status
    return {
        "message": message
    }


@router.post("/{user_id}/subscriptions/{sub_id}/cancel")
async def cancel_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        _auth=Security(verify_bearer_token)
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await cancel_subscription(sub_id, user_id)
    response.status_code = status
    return {
        "message": message
    }


@router.post("/{user_id}/subscriptions/{sub_id}/renew")
async def renew_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: RenewSubscriptionAPIPayload,
        _auth=Security(verify_bearer_token)
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await renew_subscription(sub_id, user_id, payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }
