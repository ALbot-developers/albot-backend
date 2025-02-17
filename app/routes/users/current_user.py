from fastapi import APIRouter, Security, Request, Response, HTTPException

from app import constants
from app.core.auth import verify_session
from app.external.discord.models import UserPIIResponse
from app.schemas.api_data import UserInfoData, SubscriptionsData, GuildsListData, GuildInfoData, URLData
from app.schemas.api_response import UserInfoAPIResponse, ListSubscriptionsAPIResponse, PlainAPIResponse, \
    GuildsListAPIResponse, GuildInfoAPIResponse, URLAPIResponse
from app.schemas.checkout_session import CheckoutSessionCreate
from app.schemas.subscription import SubscriptionActivate, SubscriptionRenew
from app.services import subscriptions
from app.services import user
from app.services.stripe import create_checkout_session

router = APIRouter()


@router.get("/info", response_model=UserInfoAPIResponse)
async def get_user_info_api(request: Request, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    return UserInfoAPIResponse(
        message="Fetched user info.",
        data=UserInfoData(
            info=user_info
        )
    )


@router.get("/subscriptions", response_model=ListSubscriptionsAPIResponse)
async def list_subscriptions_api(request: Request, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    return ListSubscriptionsAPIResponse(
        message="Fetched subscriptions.",
        data=SubscriptionsData(
            subscriptions=await subscriptions.list_by_user(int(user_info.id))
        )
    )


@router.post("/subscriptions/{sub_id}/activate", response_model=PlainAPIResponse)
async def activate_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        payload: SubscriptionActivate,
        _auth=Security(verify_session)
):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await subscriptions.activate(sub_id, int(user_info.id), payload.guild_id)
    response.status_code = status
    return PlainAPIResponse(message=message)


@router.post("/subscriptions/{sub_id}/cancel", response_model=PlainAPIResponse)
async def cancel_subscriptions_api(
        sub_id: str,
        request: Request,
        response: Response,
        _auth=Security(verify_session)
):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await subscriptions.cancel(sub_id, int(user_info.id))
    response.status_code = status
    return PlainAPIResponse(message=message)


@router.post("/subscriptions/{sub_id}/renew", response_model=PlainAPIResponse)
async def renew_subscriptions_api(
        sub_id: str,
        payload: SubscriptionRenew,
        request: Request,
        response: Response,
        _auth=Security(verify_session)
):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    status, message = await subscriptions.renew(sub_id, int(user_info.id), payload.new_plan)
    response.status_code = status
    return PlainAPIResponse(message=message)


@router.get("/guilds", response_model=GuildsListAPIResponse)
async def list_user_guilds(request: Request, mutual: bool = True, _auth=Security(verify_session)):
    # ?mutual=True: get only mutual guilds with our bot
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    return GuildsListAPIResponse(
        message="Fetched guilds.",
        data=GuildsListData(
            guilds=await user.get_guilds(int(user_info.id), mutual=mutual)
        )
    )


@router.get("/guilds/{guild_id}/info", response_model=GuildInfoAPIResponse)
async def get_guild_info(request: Request, guild_id: int, _auth=Security(verify_session)):
    user_info: UserPIIResponse = UserPIIResponse.from_dict(request.session["user_info"])
    return GuildInfoAPIResponse(
        message="Fetched guild info.",
        data=GuildInfoData(
            info=await user.get_guild(int(user_info.id), guild_id)
        )
    )


@router.post("/checkout-session", response_model=URLAPIResponse)
async def checkout_session(payload: CheckoutSessionCreate, request: Request, response: Response,
                           _auth=Security(verify_session)):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    if payload.plan not in constants.PRICE_IDS:
        raise HTTPException(status_code=400, detail="Invalid plan.")
    stripe_session = create_checkout_session(int(user_info.id), payload.plan)
    return URLAPIResponse(
        message="Created checkout session.",
        data=URLData(
            url=stripe_session.url
        )
    )
