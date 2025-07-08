from datetime import datetime

from fastapi import APIRouter, Depends

from app.constants import SHARD_COUNT
from app.core.dependencies import verify_turnstile
from app.external import discord
from app.schemas.api_response import PlainAPIResponse
from app.schemas.quick_report import QuickReportPost
from app.services import quick_reports

router = APIRouter()


# @router.get("/{guild_id}/quick_reports", response_model=DictAPIResponse)
# async def get_guild_dict_api(guild_id: int, _auth=Security(verify_all_tokens)):
#     pass


@router.post("/{guild_id}/quick_reports", response_model=PlainAPIResponse)
async def post_quick_report(
        guild_id: int,
        data: QuickReportPost,
        _: bool = Depends(verify_turnstile)
):
    report_id = await quick_reports.create(guild_id, data.category, data.description)
    # todo: controllerに切り分ける
    shard_id = (int(guild_id) >> 22) % int(SHARD_COUNT)
    await discord.rest_api.push_webhook(content={"embeds": [{
        "title": f"カテゴリ：{data.category}",
        "description": f"{data.description}\n\nサーバーID：{guild_id}\nシャードID：{shard_id}",
        "footer": {"text": f"{datetime.now().isoformat()}・id: {report_id}"}
    }]})
    return PlainAPIResponse(
        message="Created a report."
    )
