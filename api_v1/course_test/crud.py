import time
from typing import List

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course_test.schemas import ResultTest
from api_v1.questions import crud as crud_question
from core.models import Test, TestQuestionAssociation, TestProgress
from core.models.test_progress import TestProgressResult


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


# timelimit брать из теста
# Делать проверку на студента
async def access_activation(
    test_id: int,
    user_id: int,
    timelimit: int,
    deadline_date,
    session: AsyncSession,
):
    test = await get_test(test_id=test_id, session=session)
    progress_test = await get_progress_test(test_id=test_id, session=session)

    if progress_test:
        return progress_test

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
        participant_id=user_id,
        status=1,
        timelimit=timelimit,
        result_test=questions,
        deadline_date=deadline_date,
    )
    session.add(test_progress)
    await session.commit()

    return progress_test


async def get_progress_test(
    test_id: int,
    session: AsyncSession,
):
    test = await session.scalar(
        select(TestProgress)
        .where(TestProgress.test_id == test_id)
        .options(selectinload(TestProgress.result_test))
    )

    if not test:
        return test

    if test.status == 1 and int(time.time()) > test.deadline_date:
        test.status = 4
        test.remaining_time = 0
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
        if remaining_time <= 0:
            test.status = 3
            test.remaining_time = 0
        else:
            test.remaining_time = remaining_time

    return test


async def start_test(
    test_id: int,
    session: AsyncSession,
):
    test = await get_progress_test(session=session, test_id=test_id)

    if test.status != 1:
        return test

    if test:
        test.status = 2
        test.attempt_date = int(time.time())

    session.add(test)
    await session.commit()
    return test


async def completion_test(
    test_id: int, session: AsyncSession, result_test: List[ResultTest]
):
    test = await get_progress_test(session=session, test_id=test_id)

    if test.status != 2:
        return test

    if test:
        test.status = 3
        count_current_answer = 0

        for i, res in enumerate(result_test):
            if res.student_answer == res.correct_answer:
                count_current_answer += 1
            test.result_test[i].student_answer = res.student_answer

        test.count_current_answer = count_current_answer

    session.add(test)
    await session.commit()
    return test
