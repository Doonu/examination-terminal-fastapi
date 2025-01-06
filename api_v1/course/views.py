from fastapi import APIRouter, Depends, Form
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_user_id_in_access_token
from api_v1.course import crud as course_crud
from api_v1.course.dependencies import get_course_by_id
from api_v1.course.schemas import CourseGet, CourseUpdatePartial
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
    user_id: int = Depends(get_user_id_in_access_token),
    name: str = Form(),
    description: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.create_course(
        session=session, user_id=user_id, name=name, description=description
    )


@router.get("/{course_id}", response_model=CourseGet)
async def get_item_course(
    course: CourseGet = Depends(get_course_by_id),
):
    return course


@router.patch("/{course_id}")
async def update_course(
    course_update: CourseUpdatePartial,
    course: CourseGet = Depends(get_course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.update_course(
        course=course, session=session, course_update=course_update
    )


@router.post("/{course_id}/add_student")
async def add_student_course(
    student_id: int,
    course: CourseGet = Depends(get_course_by_id),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await course_crud.add_student_in_course(
        course=course, session=session, student_id=student_id
    )
