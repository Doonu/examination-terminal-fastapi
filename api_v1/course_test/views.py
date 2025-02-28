from typing import List

from fastapi import APIRouter, Depends, Form, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.decorators import role_required
from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.course.dependencies import get_course_by_id
from api_v1.course.schemas import CourseGet
from api_v1.course_test import crud as test_crud
from api_v1.course_test.dependencies import get_test
from api_v1.course_test.schemas import TestGet
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
    test: TestGet = Depends(get_test),
):
    return test


@router.post("/")
@role_required("Преподаватель")
async def create_test(
    request: Request,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
    name_test: str = Form(),
    time_limit: int = Form(),
):
    return await test_crud.create_test(
        session=session, user_id=user_id, name=name_test, time_limit=time_limit
    )


@router.post("/{test_id}/add_questions")
@role_required("Преподаватель")
async def add_questions_in_test(
    request: Request,
    questions: List[QuestionBase],
    test: TestGet = Depends(get_test),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.add_questions_in_test(
        test=test, session=session, questions=questions
    )


@router.post("/{test_id}/access_activation")
@role_required("Преподаватель")
async def access_activation(
    request: Request,
    deadline_date: int,
    test: TestGet = Depends(get_test),
    course: CourseGet = Depends(get_course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_crud.access_activation(
        course=course,
        session=session,
        test=test,
        deadline_date=deadline_date,
    )
