from fastapi import APIRouter, Security

from app.core.auth import verify_bearer_token
from app.schemas.api_response import PlainAPIResponse
from app.schemas.metrics import MetricsPost
from app.services import metrics

router = APIRouter()


@router.post("/{shard_id}/metrics", response_model=PlainAPIResponse)
async def post_metrics(
        shard_id: int,
        payload: MetricsPost,
        _auth=Security(verify_bearer_token)
):
    await metrics.update(shard_id, payload.connected, payload.guilds)
    return PlainAPIResponse(
        message="Updated metrics."
    )
