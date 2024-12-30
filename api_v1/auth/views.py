from fastapi import APIRouter, Depends, Form
from pydantic import EmailStr
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import User, db_helper, Profile, Role

router = APIRouter(tags=["Auth"])


@router.get('/profile')
async def pf(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    state = select(Profile).options(joinedload(Profile.role)).order_by(Profile.id)
    result: Result = await session.execute(state)
    profiles = result.scalars().all()
    return list(profiles)


@router.get('/')
async def auth(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    state = select(User).order_by(User.id)
    result: Result = await session.execute(state)
    users = result.scalars().all()
    return list(users)


@router.post('/role')
async def auth(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    role = Role(name="Студент")
    session.add(role)
    await session.commit()


@router.get('/role')
async def auth(session: AsyncSession = Depends(db_helper.scoped_session_dependency)):
    state = select(Role).order_by(Role.id)
    result: Result = await session.execute(state)
    users = result.scalars().all()
    return list(users)


@router.post('/registration')
async def auth_registration(
    email: EmailStr = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    role = await session.get(Role, ident=1)

    profile = Profile(email="user@example.com", role_id=role.id)
    session.add(profile)
    await session.flush()

    user = User(email=email, password=password.encode("utf-8"), profile_id=profile.id)
    session.add(user)
    await session.commit()
    return user