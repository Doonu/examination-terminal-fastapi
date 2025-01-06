from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.course import crud as course_crud
from api_v1.course.schemas import CourseGet
from core.models import db_helper

http_bearer = HTTPBearer()
router = APIRouter(tags=["Course"], dependencies=[Depends(http_bearer)])


@router.get("/", response_model=list[CourseGet])
async def get_course(
    user_id: int = Depends(get_user_id_in_access_token),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.get_list_course(session=session, user_id=user_id)


@router.post("/")
async def create_course(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.create_course(session=session)


@router.post("/add_student/{course_id}")
async def add_student_course(
    student_id: int,
    course_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.add_student_in_course(
        course_id=course_id, session=session, student_id=student_id
    )
