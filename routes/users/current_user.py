from fastapi import APIRouter, Security, Request, Response

from type_specifications.api_payload import ActivateSubscriptionAPIPayload, RenewSubscriptionAPIPayload
from utils.auth import verify_jwt_token
from utils.subscription import activate_subscription, cancel_subscription, renew_subscription, list_user_subscriptions

router = APIRouter()


@router.get("/subscriptions")
async def list_subscriptions_api(request: Request, _auth=Security(verify_jwt_token)):
    user_id: int = request.session["user_id"]
    subscriptions = await list_user_subscriptions(user_id)
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": subscriptions
        }
    }


@router.post("/subscriptions/{sub_id}/activate")
async def activate_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        payload: ActivateSubscriptionAPIPayload,
        _auth=Security(verify_jwt_token)
):
    status, message = await activate_subscription(sub_id, request.session["user_id"], payload.guild_id)
    response.status_code = status
    return {
        "message": message
    }


@router.post("/subscriptions/{sub_id}/cancel")
async def cancel_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        _auth=Security(verify_jwt_token)
):
    status, message = await cancel_subscription(sub_id, request.session["user_id"])
    response.status_code = status
    return {
        "message": message
    }


@router.post("/subscriptions/{sub_id}/renew")
async def renew_subscriptions_api(
        sub_id: str,
        payload: RenewSubscriptionAPIPayload,
        request: Request,
        response: Response,
        _auth=Security(verify_jwt_token)
):
    status, message = await renew_subscription(sub_id, request.session["user_id"], payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }
