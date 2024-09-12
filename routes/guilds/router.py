from fastapi import APIRouter

from routes.guilds import dict_api

router = APIRouter()
router.include_router(dict_api.router)
