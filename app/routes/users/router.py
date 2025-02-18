from fastapi import APIRouter

from app.routes.users import public, current_user

router = APIRouter()

router.include_router(current_user.router, prefix="/me")
router.include_router(public.router)
