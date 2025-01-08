from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.questions.schemas import QuestionUpdatePartial
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


async def update_question(
    question_update: QuestionUpdatePartial, session: AsyncSession, question
):
    for name, value in question_update.model_dump(exclude_unset=True).items():
        setattr(question, name, value)

    await session.commit()
    return question
