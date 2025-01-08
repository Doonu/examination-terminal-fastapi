from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Question, db_helper


async def get_item_question(
    question_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    question = await session.get(Question, question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question
