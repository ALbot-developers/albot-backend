from fastapi import APIRouter

from routes.users import current_user, public

router = APIRouter()

router.include_router(current_user.router, prefix="/me")
router.include_router(public.router)
