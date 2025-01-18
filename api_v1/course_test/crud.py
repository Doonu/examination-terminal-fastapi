import datetime
import time
from typing import List

import pytz
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import HTTPException, status
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course.schemas import CourseGet
from api_v1.course_test.scheduled_task import scheduled_test_progress_overdue

from api_v1.course_test.schemas import ResultTest
from api_v1.questions import crud as crud_question
from core.models import Test, TestQuestionAssociation, TestProgress, db_helper
from core.models.test_progress import TestProgressResult


scheduler = AsyncIOScheduler(timezone="UTC")
scheduler.start()


async def get_test(session: AsyncSession, test_id: int):
    return await session.scalar(
        select(Test)
        .where(Test.id == test_id)
        .options(
            selectinload(Test.questions).joinedload(TestQuestionAssociation.question)
        )
    )


async def get_list_test(session: AsyncSession, user_id: int):
    state = (
        select(Test)
        .where(Test.creator_id == user_id)
        .options(
            selectinload(Test.questions).joinedload(TestQuestionAssociation.question)
        )
    )
    result: Result = await session.execute(state)
    tests = result.scalars().all()
    return list(tests)


async def create_test(session: AsyncSession, user_id: int, name: str, time_limit: int):
    test = Test(name=name, time_limit=time_limit, creator_id=user_id)
    session.add(test)
    await session.commit()
    return test


async def add_questions_in_test(
    test_id: int,
    session: AsyncSession,
    questions,
):
    test = await get_test(test_id=test_id, session=session)

    for question_in in questions:
        question = await crud_question.create_question(
            session=session, question_in=question_in
        )
        test.questions.append(TestQuestionAssociation(question=question))

    await session.commit()


async def access_activation(
    test_id: int,
    deadline_date,
    course: CourseGet,
    session: AsyncSession,
):
    test = await get_test(test_id=test_id, session=session)

    for student in course.students:
        questions = [
            TestProgressResult(
                test_progress_id=test_id,
                text_question=association.question.text_question,
                options=association.question.options,
                correct_answer=association.question.correct_answer,
                student_answer=None,
            )
            for association in test.questions
        ]

        test_progress = TestProgress(
            test_id=test_id,
            status=1,
            timelimit=test.time_limit,
            result_test=questions,
            deadline_date=deadline_date,
            participant_id=student.student.id,
        )
        session.add(test_progress)

        dt_local = datetime.datetime.fromtimestamp(deadline_date, pytz.utc)
        scheduler.add_job(
            scheduled_test_progress_overdue,
            trigger="date",
            run_date=dt_local,
            args=[test_progress.test_id, test_progress.participant_id],
        )

    await session.commit()


async def start_test(progress_test, session: AsyncSession):
    if progress_test.status != 1:
        return progress_test

    if progress_test:
        progress_test.status = 2
        progress_test.attempt_date = int(time.time())

    session.add(progress_test)
    await session.commit()
    return progress_test


async def completion_test(
    progress_test, session: AsyncSession, result_test: List[ResultTest]
):
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
