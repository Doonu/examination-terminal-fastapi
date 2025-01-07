from typing import Annotated

from fastapi import Path, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

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
    return await session.scalar(
        select(Course)
        .where(Course.id == course_id)
        .options(selectinload(Course.tests).joinedload(CourseTestAssociation.test))
        .options(
            selectinload(Course.students).joinedload(CourseStudentAssociation.student)
        )
    )
