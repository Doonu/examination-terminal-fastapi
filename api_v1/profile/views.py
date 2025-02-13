from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.profile import crud as profile_crud
from api_v1.profile.schemas import ProfileGet, ProfileUpdate
from core.models import db_helper

http_bearer = HTTPBearer()
router = APIRouter(tags=["Profile"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=list[ProfileGet])
async def get_list_profile(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await profile_crud.get_list_profile(session=session)


@router.get("/me", response_model=ProfileGet)
async def get_profile(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await profile_crud.get_profile(session=session, user_id=user_id)


@router.patch("/", response_model=ProfileGet)
async def update_profile(
    profile_update: ProfileUpdate,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await profile_crud.update_profile(
        profile_update=profile_update, session=session, user_id=user_id
    )
