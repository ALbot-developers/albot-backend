import asyncpg
from fastapi import APIRouter, Security, Request, Response

from type_specifications.api_payload import SubscriptionAPIPayload
from type_specifications.database import SubscriptionData
from utils.auth import verify_token
from utils.db_connection import get_connection_pool
from utils.subscription import activate_subscription, cancel_subscription

router = APIRouter()


async def subscription_exists(user_id: int, sub_id: str):
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        row = await conn.fetchrow("SELECT * FROM subscriptions WHERE user_id=$1 and sub_id=$2", user_id, sub_id)
        return row is not None


@router.get("/")
async def get_subscriptions_api(request: Request, _auth=Security(lambda: verify_token("jwt"))):
    user_id: int = request.session["user_id"]
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        res = await conn.fetch("SELECT * FROM subscriptions WHERE user_id = $1", user_id)
        subscriptions = []
        for row in res:
            subscription = SubscriptionData.from_dict(dict(row))
            subscriptions.append(subscription)
    return {
        "message": "Fetched subscriptions.",
        "data": {
            "subscriptions": subscriptions
        }
    }


@router.post("/{sub_id}/activate")
async def activate_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        payload: SubscriptionAPIPayload,
        _auth=Security(lambda: verify_token("jwt"))
):
    if not await subscription_exists(request.session["user_id"], sub_id):
        response.status_code = 400
        return {
            "message": "Subscription not found."
        }
    res = await activate_subscription(sub_id, payload.guild_id)
    if not res:
        response.status_code = 400
        return {
            "message": "Failed to activate subscription."
        }
    return {
        "message": "Successfully activated."
    }


@router.post("/{sub_id}/cancel")
async def cancel_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        _auth=Security(lambda: verify_token("jwt"))
):
    if not await subscription_exists(request.session["user_id"], sub_id):
        response.status_code = 400
        return {
            "message": "Subscription not found."
        }
    res = await cancel_subscription(sub_id)
    if not res:
        response.status_code = 400
        return {
            "message": "Failed to activate subscription."
        }
    return {
        "message": "Successfully canceled."
    }
