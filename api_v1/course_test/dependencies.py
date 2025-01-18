from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import db_helper, Test, TestQuestionAssociation


async def get_test(
    test_id: int, session: AsyncSession = Depends(db_helper.scoped_session_dependency)
):
    return await session.scalar(
        select(Test)
        .where(Test.id == test_id)
        .options(
            selectinload(Test.questions).joinedload(TestQuestionAssociation.question)
        )
    )
