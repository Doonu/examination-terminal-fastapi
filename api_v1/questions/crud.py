from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question


async def create_question(session: AsyncSession, question_in):
    question = Question(
        text_question=question_in.text_question,
        options=question_in.options,
        correct_answer=question_in.correct_answer,
    )
    session.add(question)
    await session.flush()
    return question
