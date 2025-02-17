from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.api_response import ConnectionCommandAPIResponse, PlainAPIResponse
from app.schemas.connection_command import ConnectionCommand
from app.services import connection_commands

router = APIRouter()

@router.get("/{guild_id}/connection_command", response_model=ConnectionCommandAPIResponse)
async def get_guild_connection_command(
        guild_id: int,
        _auth=Security(verify_all_tokens)
):
    command = await connection_commands.get_by_guild(guild_id)
    return ConnectionCommandAPIResponse(
        message="Fetched connection command.",
        data=ConnectionCommand(command=command if command else "t.con")
    )


@router.put("/{guild_id}/connection_command", response_model=PlainAPIResponse)
async def update_guild_connection_command(
        guild_id: int,
        payload: ConnectionCommand,
        _auth=Security(verify_all_tokens)
):
    await connection_commands.update(guild_id, payload.command)
    return PlainAPIResponse(
        message="Updated connection command."
    )
