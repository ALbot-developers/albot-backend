from fastapi import APIRouter

from app.routes.users import public, me

router = APIRouter()

router.include_router(me.router, prefix="/me")
router.include_router(public.router)
