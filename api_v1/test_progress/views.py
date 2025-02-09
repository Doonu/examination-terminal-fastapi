from typing import List, Optional

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.decorators import role_required
from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.course_test.schemas import ResultTest
from api_v1.test_progress import crud as test_progress_crud
from api_v1.test_progress.dependencies import get_progress_test
from api_v1.test_progress.schemas import TestProgressTest
from core.models import db_helper

http_bearer = HTTPBearer()
router = APIRouter(tags=["TestProgress"], dependencies=[Depends(http_bearer)])


@router.get("/{course_id}", response_model=List[TestProgressTest])
async def get_list_progress_test_in_course(
    course_id: int,
    test_id: int,
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_progress_crud.get_list_test_progress_in_course(
        user_id=user_id, session=session, course_id=course_id, test_id=test_id
    )


@router.get("/")
async def get_list_progress_test(
    filter_date: Optional[int],
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_progress_crud.get_list_test_progress(
        user_id=user_id,
        filter_date=filter_date,
        session=session,
    )


@router.get("/{progress_test_id}", response_model=TestProgressTest)
async def get_progress_test(
    progress_test: TestProgressTest = Depends(get_progress_test),
):
    return progress_test


@router.post("/{progress_test_id}/start_test")
@role_required("Студент")
async def start_test(
    request: Request,
    progress_test: TestProgressTest = Depends(get_progress_test),
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_progress_crud.start_test(
        session=session, progress_test=progress_test, user_id=user_id
    )


@router.post("/{progress_test_id}/completion_test")
@role_required("Студент")
async def completion_test(
    request: Request,
    result_test: List[ResultTest],
    user_id: int = Depends(get_user_id_in_access_token),
    progress_test=Depends(get_progress_test),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await test_progress_crud.completion_test(
        session=session,
        result_test=result_test,
        progress_test=progress_test,
        user_id=user_id,
    )
