from fastapi import APIRouter

from routes.guilds import dict_api, settings_api, character_usage_api, trusted_roles_api, connection_command_api, \
    message_link_expand_pref_api, connection_states_api, subscriptions_api

router = APIRouter()
router.include_router(dict_api.router)
router.include_router(settings_api.router)
router.include_router(character_usage_api.router)
router.include_router(trusted_roles_api.router)
router.include_router(connection_command_api.router)
router.include_router(connection_states_api.router)
router.include_router(message_link_expand_pref_api.router)
router.include_router(subscriptions_api.router)
