from fastapi import APIRouter, Security, Response

from app.core.auth import verify_bearer_token
from app.schemas.subscription import SubscriptionActivate, SubscriptionRenew
from app.services import subscriptions

router = APIRouter()


@router.get("/{user_id}/subscriptions")
async def list_subscriptions_api(
        user_id: int,
        _auth=Security(verify_bearer_token)
):
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": await subscriptions.list_by_user(user_id)
        }
    }


@router.post("/{user_id}/subscriptions/{sub_id}/activate")
async def activate_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: SubscriptionActivate,
        _auth=Security(verify_bearer_token)
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await subscriptions.activate(sub_id, user_id, payload.guild_id)
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
    status, message = await subscriptions.cancel(sub_id, user_id)
    response.status_code = status
    return {
        "message": message
    }


@router.post("/{user_id}/subscriptions/{sub_id}/renew")
async def renew_subscriptions_api(
        user_id: int,
        sub_id: str,
        response: Response,
        payload: SubscriptionRenew,
        _auth=Security(verify_bearer_token)
):
    # BOT用APIではユーザの権限確認を行わない
    status, message = await subscriptions.renew(sub_id, user_id, payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }
