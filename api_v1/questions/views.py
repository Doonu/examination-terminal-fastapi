from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.questions import crud
from api_v1.questions.dependencies import get_item_question
from api_v1.questions.schemas import QuestionGet, QuestionUpdatePartial
from core.models import db_helper

http_bearer = HTTPBearer()
router = APIRouter(tags=["Question"], dependencies=[Depends(http_bearer)])


@router.post("/")
async def create_question(
    question_in: QuestionGet,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_question(session=session, question_in=question_in)


@router.get("/{question_id}", response_model=QuestionGet)
async def get_question(
    question: QuestionGet = Depends(get_item_question),
):
    return question


@router.patch("/{question_id}", response_model=QuestionGet)
async def update_question(
    question_update: QuestionUpdatePartial,
    question: QuestionGet = Depends(get_item_question),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.update_question(
        session=session, question_update=question_update, question=question
    )
