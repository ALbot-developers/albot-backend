from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.api_response import MessageLinkExpandAPIResponse, PlainAPIResponse
from app.schemas.message_link_expand_pref import MessageLinkExpansionPreference
from app.services import message_link_expansion

router = APIRouter()


@router.get("/{guild_id}/message_link_expand_preference", response_model=MessageLinkExpandAPIResponse)
async def get_guild_message_link_expand_pref(guild_id: int, _auth=Security(verify_all_tokens)):
    value = await message_link_expansion.is_enabled(guild_id)
    return MessageLinkExpandAPIResponse(
        message="Fetched guild data.",
        data=MessageLinkExpansionPreference(enabled=value if value is not None else False)
    )


@router.post("/{guild_id}/message_link_expand_preference", response_model=PlainAPIResponse)
async def update_guild_message_link_expand_pref(guild_id: int, data: MessageLinkExpansionPreference,
                                                _auth=Security(verify_all_tokens)):
    await message_link_expansion.set_enabled(guild_id, data.enabled)
    return PlainAPIResponse(
        message="Updated guild data."
    )
