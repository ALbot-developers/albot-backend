import json

import asyncpg
import stripe
from fastapi import APIRouter, Security, Request, Response

import constants
from models.api_payload import ActivateSubscriptionAPIPayload, RenewSubscriptionAPIPayload, \
    CheckoutSessionAPIPayload
from models.discord_api import UserPIIResponse, PartialGuild
from utils.auth import verify_session
from utils.db_connection import get_connection_pool
from utils.others import get_user_guilds
from utils.subscription import activate_subscription, cancel_subscription, renew_subscription, list_user_subscriptions

router = APIRouter()


@router.get("/info")
async def get_user_info_api(request: Request, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    return {
        "message": "Fetched user info.",
        "data": {
            "info": user_info.to_dict()
        }
    }


@router.get("/subscriptions")
async def list_subscriptions_api(request: Request, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    subscriptions = await list_user_subscriptions(int(user_info.id))
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
        _auth=Security(verify_session)
):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await activate_subscription(sub_id, int(user_info.id), payload.guild_id)
    response.status_code = status
    return {
        "message": message
    }


@router.post("/subscriptions/{sub_id}/cancel")
async def cancel_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        _auth=Security(verify_session)
):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await cancel_subscription(sub_id, int(user_info.id))
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
        _auth=Security(verify_session)
):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await renew_subscription(sub_id, int(user_info.id), payload.new_plan)
    response.status_code = status
    return {
        "message": message
    }


@router.get("/guilds")
async def list_user_guilds(request: Request, mutual: bool = True, _auth=Security(verify_session)):
    # ?mutual=True: get only mutual guilds with our bot
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    guilds = await get_user_guilds(int(user_info.id), mutual=mutual)
    return {
        "message": "Fetched guilds.",
        "data": {
            "guilds": [guild.to_dict() for guild in guilds]
        }
    }


@router.get("/guilds/{guild_id}/info")
async def get_guild_info(request: Request, guild_id: int, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    async with get_connection_pool().acquire() as conn:
        conn: asyncpg.connection.Connection
        guilds: list = json.loads(
            await conn.fetchval(
                'SELECT guilds FROM user_guilds WHERE user_id = $1',
                int(user_info.id)
            )
        )
    info = PartialGuild.from_dict([guild for guild in guilds if int(guild["id"]) == guild_id][0])
    return {
        "message": "Fetched guild data.",
        "data": {
            "info": info.to_dict()
        }
    }


@router.post("/checkout-session")
async def checkout_session(payload: CheckoutSessionAPIPayload, request: Request, response: Response,
                           _auth=Security(verify_session)):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    if payload.plan not in constants.PRICE_IDS:
        response.status_code = 400
        return {
            "message": "Invalid plan."
        }
    # create a url for `/success` and `/cancel`
    # todo: マイページのリリースに合わせて変更
    success_url = "https://albot.info/successfully-subscribed"
    cancel_url = f"https://albot.info/pricing"
    price_id = constants.PRICE_IDS[payload.plan]
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
            "discord_id": int(user_info.id),
            "plan": payload.plan
        }
    )
    return {
        "message": "Checkout session created.",
        "data": {
            "url": stripe_session.url
        }
    }
