import datetime

import pytz
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course.schemas import CourseGet
from api_v1.course_test.scheduled_task import scheduled_test_progress_overdue
from api_v1.course_test.schemas import TestGet

from api_v1.questions import crud as crud_question
from core.models import Test, TestQuestionAssociation, TestProgress
from core.models.test_progress import TestProgressResult
from scheduler import scheduler


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
    test: TestGet,
    session: AsyncSession,
    questions,
):
    for question_in in questions:
        question = await crud_question.create_question(
            session=session, question_in=question_in
        )
        test.questions.append(TestQuestionAssociation(question=question))

    await session.commit()


async def access_activation(
    test: TestGet,
    deadline_date,
    course: CourseGet,
    session: AsyncSession,
):
    for student in course.students:
        questions = [
            TestProgressResult(
                test_progress_id=test.id,
                text_question=association.question.text_question,
                options=association.question.options,
                correct_answer=association.question.correct_answer,
                student_answer=None,
            )
            for association in test.questions
        ]

        test_progress = TestProgress(
            test_id=test.id,
            course_id=course.id,
            status=1,
            timelimit=test.time_limit,
            result_test=questions,
            deadline_date=deadline_date,
            participant_id=student.student.id,
        )
        session.add(test_progress)

        await session.commit()
        scheduler.add_job(
            scheduled_test_progress_overdue,
            trigger="date",
            run_date=deadline_date,
            args=[test_progress.id],
        )

    await session.commit()
