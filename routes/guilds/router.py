from fastapi import APIRouter

from routes.guilds import dict_api, settings_api

router = APIRouter()
router.include_router(dict_api.router)
router.include_router(settings_api.router)
