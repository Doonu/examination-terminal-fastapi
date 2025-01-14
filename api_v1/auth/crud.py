from typing import Optional

from fastapi import Depends, Form, HTTPException, status
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, db_helper, Role


async def get_item_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def create_user(
    session: AsyncSession, email: EmailStr, hashed_password: bytes, profile_id: int
) -> User:
    user = User(email=email, password=hashed_password, profile_id=profile_id)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_email(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    email: EmailStr = Form(),
) -> Optional[User]:
    state = select(User).where(User.email == email)
    user = await session.scalars(state)
    return next(user, None)


async def get_role_by_name(session: AsyncSession, name: str) -> Role:
    state = select(Role).where(Role.name == name)
    role = await session.scalars(state)

    if not role:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Роль не найдена"
        )

    return next(role, None)


async def get_role_by_id(session: AsyncSession, role_id: int) -> Role:
    state = select(Role).where(Role.id == role_id)
    role = await session.scalars(state)

    if not role:
        HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Роль не найдена"
        )

    return next(role, None)
