from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.questions import crud as crud_question
from core.models import Test, TestQuestionAssociation


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
