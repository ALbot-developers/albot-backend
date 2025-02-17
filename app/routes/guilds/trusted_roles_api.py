from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.api_response import TrustedRolesResponse, PlainAPIResponse
from app.schemas.trusted_roles import TrustedRolesUpdate
from app.services import trusted_roles

router = APIRouter()


@router.get("/{guild_id}/trusted_roles", response_model=TrustedRolesResponse)
async def get_guild_trusted_roles(guild_id: int, _auth=Security(verify_all_tokens)):
    return TrustedRolesResponse(
        message="Fetched trusted roles settings.",
        data=await trusted_roles.get(guild_id)
    )


@router.put("/{guild_id}/trusted_roles", response_model=PlainAPIResponse)
async def update_guild_trusted_roles(guild_id: int, data: TrustedRolesUpdate, _auth=Security(verify_all_tokens)):
    await trusted_roles.update(guild_id, data.enabled, data.roles)
    return PlainAPIResponse(
        message="Updated trusted roles settings."
    )
