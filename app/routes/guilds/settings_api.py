from fastapi import APIRouter, Security, Depends

from app.core.auth import verify_all_tokens
from app.core.dependencies import get_subscription
from app.models.settings import PremiumSettings
from app.models.subscription import Subscription
from app.schemas.api_data import GuildSettingsData
from app.schemas.api_response import GuildSettingsAPIResponse, PlainAPIResponse
from app.schemas.guild_settings import GuildSettingsUpdate
from app.services import guild_settings
from app.services.guild_settings import get_default

router = APIRouter()


@router.get("/{guild_id}/settings", response_model=GuildSettingsAPIResponse)
async def get_guild_settings_api(guild_id: int, subscription: Subscription = Depends(get_subscription),
                                 _auth=Security(verify_all_tokens)):
    settings = await guild_settings.get(guild_id)
    if subscription is None:
        default_settings = await get_default()
        for key in PremiumSettings.__annotations__.keys():
            if key not in settings.__dict__:
                continue
            setattr(settings, key, getattr(default_settings, key))
    return GuildSettingsAPIResponse(
        message="Fetched guild data.",
        data=GuildSettingsData(
            settings=settings
        )
    )


@router.post("/{guild_id}/settings", response_model=PlainAPIResponse)
async def update_guild_settings(guild_id: int, settings: GuildSettingsUpdate,
                                subscription: Subscription = Depends(get_subscription),
                                _auth=Security(verify_all_tokens)):
    await guild_settings.update(guild_id, settings, subscription)
    return PlainAPIResponse(
        message="Updated guild data."
    )


@router.delete("/{guild_id}/settings", response_model=PlainAPIResponse)
async def delete_guild_settings(guild_id: int, _auth=Security(verify_all_tokens)):
    await guild_settings.delete(guild_id)
    return PlainAPIResponse(
        message="Deleted guild data."
    )
