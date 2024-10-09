from fastapi import APIRouter

from routes.shards import release_api, assign_api, connection_commands_api, metrics_api

router = APIRouter()
router.include_router(assign_api.router)
router.include_router(release_api.router)
router.include_router(connection_commands_api.router)
router.include_router(metrics_api.router)
