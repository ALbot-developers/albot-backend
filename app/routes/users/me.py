from fastapi import APIRouter, Security, Request, Response, UploadFile, File

from app import constants
from app.core.auth import verify_session
from app.core.error import CustomHTTPException
from app.external.discord.models import UserPIIResponse
from app.schemas.api_data import UserInfoData, SubscriptionsData, GuildsListData, GuildInfoData, URLData, VoiceModelData
from app.schemas.api_response import UserInfoAPIResponse, ListSubscriptionsAPIResponse, PlainAPIResponse, \
    GuildsListAPIResponse, GuildInfoAPIResponse, URLAPIResponse, VoiceModelAPIResponse
from app.schemas.checkout_session import CheckoutSessionCreate
from app.schemas.subscription import SubscriptionActivate, SubscriptionRenew
from app.services import subscriptions
from app.services import user
from app.services.stripe import create_checkout_session, create_customer_portal_session
from app.services.voice_clone import create_voice, save_voice_model, get_voice_model

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
        raise CustomHTTPException(status_code=400, detail="Invalid plan.")
    stripe_session = await create_checkout_session(int(user_info.id), payload.plan)
    return URLAPIResponse(
        message="Created checkout session.",
        data=URLData(
            url=stripe_session.url
        )
    )


@router.get("/customer-portal", response_model=URLAPIResponse)
async def get_customer_portal(request: Request, _auth=Security(verify_session)):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    portal_session = await create_customer_portal_session(int(user_info.id))
    if not portal_session:
        raise CustomHTTPException(status_code=400, detail="Stripe customer ID not found.")
    return URLAPIResponse(
        message="Created customer portal session.",
        data=URLData(
            url=portal_session.url
        )
    )


ALLOWED_AUDIO_TYPES = {"audio/wav", "audio/mpeg", "audio/mp3", "audio/m4a", "audio/x-m4a", "audio/mp4"}
MAX_AUDIO_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/voice-model", response_model=VoiceModelAPIResponse)
async def create_voice_model_api(request: Request, audio: UploadFile = File(...), _auth=Security(verify_session)):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])

    if audio.content_type not in ALLOWED_AUDIO_TYPES:
        raise CustomHTTPException(status_code=400, detail="Unsupported audio format. Supported: WAV, MP3, M4A.")

    audio_data = await audio.read()
    if len(audio_data) > MAX_AUDIO_SIZE:
        raise CustomHTTPException(status_code=400, detail="Audio file too large. Maximum size is 10MB.")

    try:
        voice = await create_voice(audio_data, audio.content_type)
    except RuntimeError as e:
        raise CustomHTTPException(status_code=502, detail=str(e))

    await save_voice_model(int(user_info.id), voice)

    return VoiceModelAPIResponse(
        message="Voice model created.",
        data=VoiceModelData(voice_model=voice)
    )


@router.get("/voice-model", response_model=VoiceModelAPIResponse)
async def get_voice_model_api(request: Request, _auth=Security(verify_session)):
    user_info = UserPIIResponse.from_dict(request.session["user_info"])
    voice_model = await get_voice_model(int(user_info.id))
    return VoiceModelAPIResponse(
        message="Fetched voice model.",
        data=VoiceModelData(voice_model=voice_model)
    )
