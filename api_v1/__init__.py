from fastapi import APIRouter

from .auth.views import router as auth_router
from .role.views import router as role_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth")
router.include_router(role_router, prefix="/role")
