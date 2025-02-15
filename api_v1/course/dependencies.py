from typing import Annotated

from fastapi import Path, Depends
from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api_v1.test_progress.dependencies import get_progress_test
from core.models import (
    Course,
    CourseStudentAssociation,
    db_helper,
    CourseTestAssociation,
)


async def get_course_by_id(
    course_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    course = await session.scalar(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.tests).joinedload(CourseTestAssociation.test))
        .options(
            selectinload(Course.students).joinedload(CourseStudentAssociation.student)
        )
    )

    for test in course.tests:
        progress_test = await get_progress_test(
            session=session, test_id=test.test.id, course_id=course_id
        )

        if progress_test:
            test.test.access_test = True
        else:
            test.test.access_test = False

    return course
