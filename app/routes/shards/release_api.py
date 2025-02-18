from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.api_response import PlainAPIResponse
from app.services import shards

router = APIRouter()


@router.post("/{shard_id}/release", response_model=PlainAPIResponse)
async def release_shard(shard_id: int, _auth=Security(verify_bearer_token)):
    await shards.release(shard_id)
    return PlainAPIResponse(
        message="Shard released."
    )
