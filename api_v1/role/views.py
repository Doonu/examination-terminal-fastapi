from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.role import crud
from core.models import db_helper

router = APIRouter(tags=["Role"])


@router.get("/")
async def get_role_list(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_role_list(session=session)


@router.post("/")
async def create_role(
    role_name: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_role(session=session, role_name=role_name)
