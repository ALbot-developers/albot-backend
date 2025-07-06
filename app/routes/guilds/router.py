from fastapi import APIRouter, Security, BackgroundTasks

from app.core.auth import verify_bearer_token
from app.routes.guilds import dict_api, connection_command_api, subscriptions_api, settings_api, \
    connection_states_api, trusted_roles_api, character_usage_api, message_link_expand_pref_api, quick_reports_api
from app.schemas.api_response import PlainAPIResponse
from app.services import guild_resources, logs

router = APIRouter()
router.include_router(dict_api.router)
router.include_router(settings_api.router)
router.include_router(character_usage_api.router)
router.include_router(trusted_roles_api.router)
router.include_router(connection_command_api.router)
router.include_router(connection_states_api.router)
router.include_router(message_link_expand_pref_api.router)
router.include_router(subscriptions_api.router)
router.include_router(quick_reports_api.router)


@router.post("/{guild_id}", response_model=PlainAPIResponse)
async def create_guild_resources(
        guild_id: int,
        background_tasks: BackgroundTasks,
        _auth=Security(verify_bearer_token)
):
    await guild_resources.create(guild_id)
    # noinspection PyTypeChecker
    background_tasks.add_task(logs.record_guild_event, guild_id, 'join')
    return PlainAPIResponse(
        message="Created guild resources."
    )


@router.delete("/{guild_id}", response_model=PlainAPIResponse)
async def delete_guild_resources(
        guild_id: int,
        background_tasks: BackgroundTasks,
        _auth=Security(verify_bearer_token)
):
    await guild_resources.delete(guild_id)
    # noinspection PyTypeChecker
    background_tasks.add_task(logs.record_guild_event, guild_id, 'leave')
    return PlainAPIResponse(
        message="Deleted guild resources."
    )
