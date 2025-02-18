from typing import Literal

from fastapi import APIRouter, Security

from app.core.auth import verify_session
from app.routes.shards import metrics_api, release_api, assign_api, connection_commands_api
from app.schemas.api_data import ShardsListData
from app.schemas.api_response import ShardsListAPIResponse
from app.services import shards

router = APIRouter()
router.include_router(assign_api.router)
router.include_router(release_api.router)
router.include_router(connection_commands_api.router)
router.include_router(metrics_api.router)


# todo: 将来的には死活監視の情報を使用
@router.get("", response_model=ShardsListAPIResponse)
async def index(
        _auth=Security(verify_session),
        status: Literal["online", "offline", "all"] = "all"
):
    return ShardsListAPIResponse(
        message="Fetched shard IDs.",
        data=ShardsListData(
            ids=await shards.list_ids(status)
        )
    )
