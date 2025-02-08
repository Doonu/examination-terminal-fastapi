import time
from typing import List

from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course_test.schemas import ResultTest
from api_v1.profile import crud as profile_crud
from api_v1.test_progress.schemas import TestProgressTest
from core.models import TestProgress


async def get_list_test_progress_in_course(
    user_id: int, test_id: int, course_id: int, session: AsyncSession
):
    user = await profile_crud.get_profile(session=session, user_id=user_id)

    if user.role.name == "Преподаватель":
        state = (
            select(TestProgress)
            .where(TestProgress.test_id == test_id)
            .where(TestProgress.course_id == course_id)
            .options(selectinload(TestProgress.result_test))
        )
    else:
        state = (
            select(TestProgress)
            .where(TestProgress.course_id == course_id)
            .where(TestProgress.participant_id == user_id)
            .options(selectinload(TestProgress.result_test))
        )

    result: Result = await session.execute(state)
    test_progress_list = result.scalars().all()
    return list(test_progress_list)


async def get_list_test_progress(user_id: int, test_id: int, session: AsyncSession):
    user = await profile_crud.get_profile(session=session, user_id=user_id)

    state = (
        select(TestProgress)
        .where(TestProgress.participant_id == user_id)
        .options(selectinload(TestProgress.result_test))
    )

    result: Result = await session.execute(state)
    test_progress_list = result.scalars().all()
    return list(test_progress_list)


async def start_test(
    progress_test: TestProgressTest, user_id: int, session: AsyncSession
):
    if progress_test.participant_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для прохождения теста",
        )

    if progress_test.status != 1:
        return progress_test

    if progress_test:
        progress_test.status = 2
        progress_test.attempt_date = int(time.time())

    session.add(progress_test)
    await session.commit()
    return progress_test


async def completion_test(
    progress_test, user_id: int, result_test: List[ResultTest], session: AsyncSession
):
    if progress_test.participant_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для завершения теста",
        )

    if progress_test.status != 2:
        return progress_test

    if progress_test.status == 4:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Вышло время на прохождение текста",
        )

    if progress_test:
        progress_test.status = 3
        count_current_answer = 0

        for i, res in enumerate(result_test):
            if res.student_answer == res.correct_answer:
                count_current_answer += 1
            progress_test.result_test[i].student_answer = res.student_answer

        progress_test.count_current_answer = count_current_answer

    session.add(progress_test)
    await session.commit()
    return progress_test
