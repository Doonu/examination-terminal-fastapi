import time
from typing import Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.test_progress.crud import completion_test
from core.models import TestProgress, db_helper


async def get_progress_test(
    progress_test_id: Optional[int] = None,
    test_id: Optional[int] = None,
    course_id: Optional[int] = None,
    user_id: Optional[int] = None,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    state = select(TestProgress).options(selectinload(TestProgress.result_test))

    if user_id:
        state = state.where(TestProgress.participant_id == user_id)

    if progress_test_id:
        state = state.where(TestProgress.id == progress_test_id)

    if test_id:
        state = state.where(TestProgress.test_id == test_id)

    if course_id:
        state = state.where(TestProgress.course_id == course_id)

    test_progress = await session.scalar(state)

    if not test_progress:
        return None

    if (
        test_progress.status == 1
        or test_progress.status == 3
        or test_progress.status == 4
    ):
        return test_progress

    end_date = (
        test_progress.deadline_date
        if test_progress.attempt_date > test_progress.deadline_date
        else test_progress.attempt_date
    )

    if end_date < int(time.time()):
        await completion_test(
            progress_test=test_progress,
            user_id=user_id,
            result_test=test_progress.result_test,
            session=session,
        )
        return

    remaining_time = end_date - (int(time.time()) + int(test_progress.timelimit))

    if test_progress.status == 2:
        test_progress.remaining_time = remaining_time

    return test_progress
