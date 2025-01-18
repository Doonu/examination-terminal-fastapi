import pytest

from api_v1.auth.views_test import registration_test, auth_login_test
from api_v1.course.views_test import create_course_test, get_course_test
from api_v1.course_test.views_test import (
    create_test_item_test,
    create_questions_and_add_in_test,
    add_test_in_course_test,
    add_student_in_course_test,
    access_activation_test,
)
from api_v1.profile.views_test import get_profile_test
from api_v1.role.views_test import get_role_list_test, create_role_test
from api_v1.test_progress.views_test import (
    get_progress_test,
    start_test_test,
    completion_test,
    get_progress_test_complete,
)
from tests.course_test.constants import (
    role_teacher,
    role_student,
    email_student,
    role_student_id,
    password_student,
    email_teacher,
    role_teacher_id,
    password_teacher,
    id_teacher,
    name_course,
    description_course,
    name_test,
    limit,
    id_test,
    questions,
    id_course,
    id_student,
    deadline_date,
    result_test,
    count_current_answer,
    progress_id_test,
)


@pytest.mark.asyncio
async def test_course_test(async_client):
    await get_role_list_test(async_client, role_list=[])
    await create_role_test(async_client, role_id=1, name=role_teacher)
    await create_role_test(async_client, role_id=2, name=role_student)
    await registration_test(
        async_client,
        email=email_student,
        role_id=role_student_id,
        password=password_student,
    )
    await registration_test(
        async_client,
        email=email_teacher,
        role_id=role_teacher_id,
        password=password_teacher,
    )
    await get_profile_test(async_client, profile_id=id_teacher, email=email_teacher)

    await create_course_test(
        async_client, name=name_course, description=description_course
    )
    await create_test_item_test(async_client, name=name_test, time_limit=limit)
    await create_questions_and_add_in_test(
        async_client, test_id=id_test, questions=questions
    )

    await add_test_in_course_test(async_client, course_id=id_course, test_ids=[id_test])
    await add_student_in_course_test(
        async_client, course_id=id_course, student_ids=[id_student]
    )

    await get_course_test(
        async_client,
        course_id=id_course,
        name=name_course,
        description=description_course,
        teacher_id=id_teacher,
    )

    await access_activation_test(
        async_client, test_id=id_test, deadline_date=deadline_date, course_id=id_course
    )

    await auth_login_test(async_client, email=email_student, password=password_student)
    await get_progress_test(
        async_client,
        progress_test_id=progress_id_test,
        status=1,
        name_test=name_test,
        deadline_date=deadline_date,
        teacher_id=id_teacher,
    )

    await start_test_test(async_client, progress_test_id=progress_id_test)
    await get_progress_test(
        async_client,
        status=2,
        name_test=name_test,
        deadline_date=deadline_date,
        teacher_id=id_teacher,
        progress_test_id=progress_id_test,
    )
    await completion_test(
        async_client, progress_test_id=progress_id_test, result_test=result_test
    )
    await get_progress_test_complete(
        async_client,
        progress_test_id=progress_id_test,
        count_current_answer=count_current_answer,
    )
