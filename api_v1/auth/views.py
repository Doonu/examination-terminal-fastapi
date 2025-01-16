from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.dependencies import (
    validate_auth_user,
    register_user,
    create_tokens_by_auth,
    get_current_auth_user_for_refresh,
    create_access_token,
)
from ..auth.schemas import AuthBase
from core.models import User, db_helper

router = APIRouter(tags=["Auth"])


@router.post("/login", response_model=AuthBase)
async def auth_login(
    user: User = Depends(validate_auth_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_tokens_by_auth(user=user, session=session)


@router.post("/registration")
async def auth_registration(
    user: User = Depends(register_user),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await create_tokens_by_auth(user=user, session=session)


@router.post("/refresh", response_model=AuthBase, response_model_exclude_none=True)
async def auth_refresh(user: User = Depends(get_current_auth_user_for_refresh)):
    access_token = await create_access_token(user=user)
    return AuthBase(access_token=access_token, token_type="Bearer")


# @router.get("/")
# async def auth(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
#     state = select(User).order_by(User.id)
#     result: Result = await session.execute(state)
#     users = result.scalars().all()
#     return list(users)
