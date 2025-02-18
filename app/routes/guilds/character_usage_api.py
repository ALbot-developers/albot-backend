from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens, verify_bearer_token
from app.schemas.api_response import CharacterUsageAPIResponse, PlainAPIResponse
from app.schemas.character_usage import CharacterUsagesUpdate
from app.services import character_usages

router = APIRouter()


@router.get("/{guild_id}/character_usage", response_model=CharacterUsageAPIResponse)
async def get_guild_character_usage_api(guild_id: int, _auth=Security(verify_all_tokens)):
    return CharacterUsageAPIResponse(
        message="Fetched guild data.",
        data=await character_usages.get(guild_id)
    )


@router.post("/{guild_id}/character_usage", response_model=PlainAPIResponse)
async def update_guild_character_usage(
        guild_id: int, payload: CharacterUsagesUpdate,
        _auth=Security(verify_bearer_token)
):
    # update used characters
    if payload.wavenet:
        await character_usages.update(guild_id, "wavenet", payload.wavenet)
    if payload.standard:
        await character_usages.update(guild_id, "standard", payload.standard)
    return PlainAPIResponse(
        message="Updated guild data."
    )
