from fastapi import APIRouter, Depends

from app.core.dependencies import verify_turnstile
from app.schemas.api_response import PlainAPIResponse
from app.schemas.quick_report import QuickReportPost
from app.services import quick_reports

router = APIRouter()


# @router.get("/{guild_id}/quick-report", response_model=DictAPIResponse)
# async def get_guild_dict_api(guild_id: int, _auth=Security(verify_all_tokens)):
#     pass


@router.post("/{guild_id}/quick-reports", response_model=PlainAPIResponse)
async def post_quick_report(
        guild_id: int,
        data: QuickReportPost,
        _: bool = Depends(verify_turnstile)
):
    report_id = await quick_reports.create(guild_id, data.category, data.description)
    # todo: send a discord notification
    return PlainAPIResponse(
        message="Created a report."
    )
