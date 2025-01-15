from typing import List

from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.course.dependencies import get_course_by_id
from api_v1.course.schemas import CourseGet
from api_v1.course_test import crud as test_crud
from api_v1.course_test.schemas import TestGet, ResultTest, TestProgressTest
from api_v1.questions.schemas import QuestionBase
from core.models import db_helper

http_bearer = HTTPBearer()
router = APIRouter(tags=["Test"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=List[TestGet])
async def get_tests(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.get_list_test(session=session, user_id=user_id)


@router.get("/{test_id}", response_model=TestGet)
async def get_test(
    test_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.get_test(test_id=test_id, session=session)


@router.get("/{test_id}/progress_test", response_model=TestProgressTest)
async def get_progress_test(
    test_id: int,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.get_progress_test(
        test_id=test_id, session=session, user_id=user_id
    )


@router.post("/")
async def create_test(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    name_test: str = Form(),
    time_limit: int = Form(),
):
    return await test_crud.create_test(
        session=session, user_id=user_id, name=name_test, time_limit=time_limit
    )


@router.post("/{test_id}/add_questions")
async def add_questions_in_test(
    test_id: int,
    questions: List[QuestionBase],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.add_questions_in_test(
        test_id=test_id, session=session, questions=questions
    )


@router.post("/{test_id}/access_activation")
async def access_activation(
    test_id: int,
    deadline_date: int,
    course: CourseGet = Depends(get_course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.access_activation(
        course=course,
        session=session,
        test_id=test_id,
        deadline_date=deadline_date,
    )


@router.post("/{test_id}/start_test")
async def start_test(
    test_id: int,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.start_test(test_id=test_id, session=session, user_id=user_id)


@router.post("/{test_id}/completion_test")
async def completion_test(
    test_id: int,
    result_test: List[ResultTest],
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.completion_test(
        session=session, test_id=test_id, result_test=result_test, user_id=user_id
    )
