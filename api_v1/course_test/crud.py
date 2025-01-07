from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Test


async def get_test(session: AsyncSession, test_id: int):
    return await session.get(Test, test_id)


async def get_list_test(session: AsyncSession, user_id: int):
    state = select(Test).where(Test.creator_id == user_id)
    result: Result = await session.execute(state)
    tests = result.scalars().all()
    return list(tests)


async def create_test(session: AsyncSession, user_id: int, name: str):
    test = Test(name=name, time_limit=60, creator_id=user_id)
    session.add(test)
    await session.commit()
    return test
