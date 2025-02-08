from typing import Union, Optional

from sqlalchemy import select, Result, or_, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.course.schemas import CourseGet, CourseUpdatePartial
from api_v1.course_test.dependencies import get_test
from api_v1.profile import crud as crud_profile
from api_v1.profile.crud import get_profile
from core.models import Course, CourseStudentAssociation, CourseTestAssociation


async def create_course(
    session: AsyncSession, name: str, description: str, user_id: int
):
    course = Course(name=name, description=description, teacher_id=user_id)
    session.add(course)
    await session.commit()


async def get_list_course(session: AsyncSession, user_id: int, search: Optional[str], direct: Optional[int], sort_by: Optional[str]) -> list[CourseGet]:
    user = await get_profile(session=session, user_id=user_id)

    state = (
        select(Course)
        .options(selectinload(Course.tests).joinedload(CourseTestAssociation.test))
        .options(
            selectinload(Course.students).joinedload(CourseStudentAssociation.student)
        )
    )

    if user.role.name == "Преподаватель":
        state = state.where(Course.teacher_id == user_id)

    if user.role.name == "Студент":
        state = state.where(Course.students.any(CourseStudentAssociation.profile_id == user_id))
    
    if search:
        state = state.where(
            or_(
                Course.name.ilike(f"%{search}%"),
                Course.description.ilike(f"%{search}%")
            )
        )

    order_func = asc if direct == 1 else desc

    sort_field = getattr(Course, sort_by, Course.name)
    state = state.order_by(order_func(sort_field))

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
