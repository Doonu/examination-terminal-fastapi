from typing import Optional

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from api_v1.profile.schemas import ProfileGet, ProfileUpdate
from core.models import Profile, db_helper


async def create_profile(session: AsyncSession, role_id: int, email: EmailStr):
    profile = Profile(email=email, role_id=role_id)
    session.add(profile)
    await session.commit()
    return profile


async def get_list_profile(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> list[ProfileGet]:
    state = select(Profile).options(joinedload(Profile.role)).order_by(Profile.id)
    result: Result = await session.execute(state)
    profiles = result.scalars().all()
    return list(profiles)


async def get_profile(user_id: int, session: AsyncSession) -> Optional[ProfileGet]:
    state = (
        select(Profile).options(joinedload(Profile.role)).where(Profile.id == user_id)
    )
    profile = await session.scalars(state)
    return next(profile, None)


async def update_profile(
    profile_update: ProfileUpdate, session: AsyncSession, user_id: int
):
    current_profile = await get_profile(user_id=user_id, session=session)
    update_data = profile_update.model_dump(exclude_unset=True).items()

    for name, value in update_data:
        setattr(current_profile, name, value)

    await session.commit()
    return current_profile
