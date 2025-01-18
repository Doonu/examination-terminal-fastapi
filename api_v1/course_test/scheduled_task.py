from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.course_test.dependencies import get_progress_test
from core.models import db_helper


async def scheduled_test_progress_overdue(progress_test_id):
    session_gen = db_helper.scoped_session_dependency()
    session: AsyncSession = await session_gen.__anext__()
    test_progress = await get_progress_test(
        session=session, progress_test_id=progress_test_id
    )

    if test_progress.status == 3:
        return

    if (
        test_progress.status == 1
        or test_progress.status == 2
        and not test_progress.result_test
    ):
        test_progress.status = 4
        await session.commit()
        return test_progress

    if test_progress.status == 2 and test_progress.result_test:
        test_progress.status = 3
        await session.commit()
        return test_progress
    elif test_progress.status == 2 and not test_progress.result_test:
        test_progress.status = 4
        await session.commit()
        return test_progress

    return
