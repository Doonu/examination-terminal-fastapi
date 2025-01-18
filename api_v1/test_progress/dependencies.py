import time

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import TestProgress, db_helper


async def get_progress_test(
    progress_test_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    test = await session.scalar(
        select(TestProgress)
        .where(TestProgress.id == progress_test_id)
        .options(selectinload(TestProgress.result_test))
    )

    if not test:
        return test

    if test.status == 1 or test.status == 3 or test.status == 4:
        return test

    end_date = (
        test.deadline_date
        if test.attempt_date > test.deadline_date
        else test.attempt_date
    )
    remaining_time = abs(int(time.time()) - (end_date + int(test.timelimit)))

    if test.status == 2:
        test.remaining_time = remaining_time

    return test
