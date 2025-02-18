from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.api_response import ShardProvisionAPIResponse
from app.services import shards

router = APIRouter()


@router.get("/assign", response_model=ShardProvisionAPIResponse)
async def assign_shard(_auth=Security(verify_bearer_token)):
    return ShardProvisionAPIResponse(
        message="Shard assigned.",
        data=await shards.provision()
    )
