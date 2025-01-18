import time

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.auth.dependencies import get_user_id_in_access_token
from core.models import TestProgress, db_helper


async def get_progress_test(
    test_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    user_id: int = Depends(get_user_id_in_access_token),
):
    test = await session.scalar(
        select(TestProgress)
        .where(TestProgress.test_id == test_id)
        .where(TestProgress.participant_id == user_id)
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
