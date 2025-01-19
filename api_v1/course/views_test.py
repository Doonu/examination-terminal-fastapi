from typing import List

from core.config import settings


async def create_course_test(async_client, name: str, description: str):
    created_course = await async_client.post(
        f"{settings.api_v1_prefix}/course/",
        data={"name": name, "description": description},
    )
    assert created_course.status_code == 200


async def get_course_test(
    async_client,
    course_id: int,
    name: str,
    description: str,
    teacher_id: int,
):
    course_list = await async_client.get(f"{settings.api_v1_prefix}/course/{course_id}")
    assert course_list.status_code == 200
    data = course_list.json()
    assert data["id"] == course_id
    assert data["name"] == name
    assert data["description"] == description
    assert data["teacher_id"] == teacher_id


async def add_test_in_course_test(async_client, course_id: int, test_ids: List[int]):
    test_in_course = await async_client.post(
        f"{settings.api_v1_prefix}/course/{course_id}/add_test",
        json=test_ids,
    )
    assert test_in_course.status_code == 200


async def add_student_in_course_test(
    async_client, course_id: int, student_ids: List[int]
):
    student_in_course = await async_client.post(
        f"{settings.api_v1_prefix}/course/{course_id}/add_student", json=student_ids
    )
    assert student_in_course.status_code == 200
