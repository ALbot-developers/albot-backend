from fastapi import APIRouter, Security

from app.core.auth import verify_all_tokens
from app.schemas.api_data import MetricsData
from app.schemas.api_response import MetricsAPIResponse
from app.services import metrics

router = APIRouter()


@router.get("", response_model=MetricsAPIResponse)
async def get_metrics():
    data = await metrics.get()
    return MetricsAPIResponse(
        message="Fetched metrics.",
        data=MetricsData(
            metrics=data
        )
    )
