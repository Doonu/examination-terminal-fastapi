from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Profile


async def create_profile(session: AsyncSession, role_id: int):
    profile = Profile(email="user@example.com", role_id=role_id)
    session.add(profile)
    await session.commit()
    return profile
