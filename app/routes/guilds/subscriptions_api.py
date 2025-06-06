from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.api_data import SubscriptionsData
from app.schemas.api_response import ListSubscriptionsAPIResponse
from app.services import subscriptions

router = APIRouter()


@router.get("/{guild_id}/subscriptions", response_model=ListSubscriptionsAPIResponse)
async def list_guild_subscriptions_api(
        guild_id: int,
        _auth=Security(verify_all_tokens)
):
    return ListSubscriptionsAPIResponse(
        message="Fetched subscriptions.",
        data=SubscriptionsData(
            subscriptions=await subscriptions.list_by_guild(guild_id)
        )
    )
