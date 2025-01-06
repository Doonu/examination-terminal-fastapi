from typing import Union

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette import status

from api_v1.course.schemas import CourseGet, CourseUpdatePartial
from api_v1.profile import crud as crud_profile
from core.models import Course, CourseStudentAssociation


async def create_course(
    session: AsyncSession, name: str, description: str, user_id: int
):
    teacher_profile = await crud_profile.get_profile(user_id=user_id, session=session)
    if not teacher_profile.role.name == "Преподаватель":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Нет прав на создание курса",
        )

    course = Course(name=name, description=description, teacher_id=user_id)
    session.add(course)
    await session.commit()


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


async def update_course(
    course: CourseGet, session: AsyncSession, course_update: CourseUpdatePartial
):
    for name, value in course_update.model_dump(exclude_unset=True).items():
        setattr(course, name, value)

    await session.commit()
    return course


async def add_student_in_course(
    student_ids: Union[int, list[int]], session: AsyncSession, course
):
    students = [
        await crud_profile.get_profile(session=session, user_id=single_id)
        for single_id in student_ids
    ]

    for student in students:
        course.students.append(CourseStudentAssociation(student=student))

    await session.commit()


async def delete_student_in_course(student_id: int, session: AsyncSession, course):
    student = await crud_profile.get_profile(session=session, user_id=student_id)
    association_to_remove = next(
        (assoc for assoc in course.students if assoc.profile_id == student.id), None
    )

    await session.delete(association_to_remove)
    await session.commit()


async def delete_course(
    course: CourseGet,
    session: AsyncSession,
):
    await session.delete(course)
    await session.commit()
