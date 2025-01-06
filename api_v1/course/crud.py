from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course.schemas import CourseGet
from api_v1.profile import crud as crud_profile
from core.models import Course, CourseStudentAssociation


# TODO: доделать
async def create_course(session: AsyncSession):
    course = Course(name="Курс по JS", description="Очень крутой курс", teacher_id=1)
    session.add(course)
    await session.commit()
    return course


async def get_list_course(session: AsyncSession, user_id: int) -> list[CourseGet]:
    state = (
        select(Course)
        .where(Course.teacher_id == user_id)
        .options(
            selectinload(Course.students).joinedload(CourseStudentAssociation.student)
        )
    )
    result: Result = await session.execute(state)
    courses = result.scalars().all()
    return list(courses)


async def get_item_course(course_id: int, session: AsyncSession):
    return await session.scalar(
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.students).joinedload(CourseStudentAssociation.student)
        )
    )


async def add_student_in_course(student_id: int, session: AsyncSession, course_id: int):
    student = await crud_profile.get_profile(session=session, user_id=student_id)
    course = await get_item_course(session=session, course_id=course_id)

    course.students.append(CourseStudentAssociation(student=student))

    await session.commit()
