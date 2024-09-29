from fastapi import APIRouter, Security, Response

from type_specifications.api_payload import ActivateSubscriptionAPIPayload, RenewSubscriptionAPIPayload
from utils.auth import verify_token
from utils.subscription import activate_subscription, cancel_subscription, renew_subscription, list_user_subscriptions

router = APIRouter()


@router.get("/{user_id}/subscriptions")
async def list_subscriptions_api(
        user_id: int,
        _auth=Security(lambda: verify_token("bearer"))
):
    subscriptions = await list_user_subscriptions(user_id)
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": subscriptions
        }
    }


@router.get("/{user_id}/subscriptions/{sub_id}/activate")
async def activate_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: ActivateSubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await activate_subscription(sub_id, user_id, payload.guild_id)
    response.status_code = status
    return {
        "message": message
    }


@router.get("/{user_id}/subscriptions/{sub_id}/cancel")
async def cancel_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await cancel_subscription(sub_id, user_id)
    response.status_code = status
    return {
        "message": message
    }


@router.get("/{user_id}/subscriptions/{sub_id}/renew")
async def renew_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: RenewSubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("bearer"))
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await renew_subscription(sub_id, user_id, payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }
