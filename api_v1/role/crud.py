from typing import List

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Role


async def get_role_list(session: AsyncSession) -> List[Role]:
    state = select(Role).order_by(Role.id)
    result: Result = await session.execute(state)
    roles = result.scalars().all()
    return list(roles)


async def create_role(session: AsyncSession, role_name: str):
    role = Role(name=role_name)
    session.add(role)
    await session.commit()
    return role
