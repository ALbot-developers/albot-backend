from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.api_data import ShardConnectionCommandsData
from app.schemas.api_response import ShardConnectionCommandsAPIResponse
from app.services import connection_commands

router = APIRouter()


@router.get("/{shard_id}/connection_commands", response_model=ShardConnectionCommandsAPIResponse)
async def get_connection_commands(
        shard_id: int,
        changes_only: bool = False,
        _auth=Security(verify_bearer_token)
):
    return ShardConnectionCommandsAPIResponse(
        message="Fetched connection commands.",
        data=ShardConnectionCommandsData(
            commands=await connection_commands.get_by_shard(
                shard_id, changes_only=changes_only
            )
        )
    )
