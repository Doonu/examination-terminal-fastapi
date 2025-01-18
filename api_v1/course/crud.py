from typing import Union

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course.schemas import CourseGet, CourseUpdatePartial
from api_v1.course_test.dependencies import get_test
from api_v1.profile import crud as crud_profile
from core.models import Course, CourseStudentAssociation, CourseTestAssociation


async def create_course(
    session: AsyncSession, name: str, description: str, user_id: int
):
    course = Course(name=name, description=description, teacher_id=user_id)
    session.add(course)
    await session.commit()


async def get_list_course(session: AsyncSession, user_id: int) -> list[CourseGet]:
    state = (
        select(Course)
        .where(Course.teacher_id == user_id)
        .options(selectinload(Course.tests).joinedload(CourseTestAssociation.test))
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


async def add_test_in_course(
    tests_ids: Union[int, list[int]], session: AsyncSession, course
):
    tests = [
        await get_test(session=session, test_id=single_id) for single_id in tests_ids
    ]

    for test in tests:
        course.tests.append(CourseTestAssociation(test=test))

    await session.commit()


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
