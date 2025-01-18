from typing import List

from api_v1.course_test.views_test import QuestionResultBase
from core.config import settings


async def get_progress_test(
    async_client,
    progress_test_id: int,
    status: int,
    deadline_date: int,
    name_test: str,
    teacher_id: int,
):
    get_progress = await async_client.get(
        f"{settings.api_v1_prefix}/test-progress/{progress_test_id}"
    )
    assert get_progress.status_code == 200
    data = get_progress.json()
    assert data["status"] == status
    assert data["deadline_date"] == deadline_date
    assert data["test"]["name"] == name_test
    assert data["test"]["creator_id"] == teacher_id


async def get_progress_test_complete(
    async_client,
    progress_test_id: int,
    count_current_answer: int,
):
    get_progress = await async_client.get(
        f"{settings.api_v1_prefix}/test-progress/{progress_test_id}"
    )
    assert get_progress.status_code == 200
    data = get_progress.json()
    assert data["count_current_answer"] == count_current_answer
    result_test_user = data.get("result_test", [])

    correct_count = sum(
        1
        for item in result_test_user
        if item["correct_answer"] == item["student_answer"]
    )

    assert (
        correct_count == count_current_answer
    ), f"Ожидалось {count_current_answer} совпадений, но найдено {correct_count}"


async def completion_test(
    async_client, progress_test_id: int, result_test: List[QuestionResultBase]
):
    completion = await async_client.post(
        f"{settings.api_v1_prefix}/test-progress/{progress_test_id}/completion_test",
        json=result_test,
    )
    assert completion.status_code == 200


async def start_test_test(
    async_client,
    progress_test_id: int,
):
    start_test = await async_client.post(
        f"{settings.api_v1_prefix}/test-progress/{progress_test_id}/start_test"
    )
    assert start_test.status_code == 200
