from typing import TypedDict, List, Optional

from core.config import settings


class QuestionBase(TypedDict):
    text_question: int
    options: List[str]
    correct_answer: str


class QuestionResultBase(QuestionBase):
    student_answer: Optional[str]


async def create_test_item_test(async_client, name: str, time_limit: int):
    item_test = await async_client.post(
        f"{settings.api_v1_prefix}/tests/",
        data={"name_test": name, "time_limit": time_limit},
    )
    assert item_test.status_code == 200


async def create_questions_and_add_in_test(
    async_client, test_id: int, questions: List[QuestionBase]
):
    create_questions_in_test = await async_client.post(
        f"{settings.api_v1_prefix}/tests/{test_id}/add_questions", json=questions
    )
    assert create_questions_in_test.status_code == 200


async def access_activation_test(
    async_client, test_id: int, deadline_date: int, course_id: int
):
    access_activation = await async_client.post(
        f"{settings.api_v1_prefix}/tests/{test_id}/access_activation",
        params={
            "deadline_date": deadline_date,
            "course_id": course_id,
        },
    )
    assert access_activation.status_code == 200


async def get_progress_test(
    async_client,
    test_id: int,
    status: int,
    deadline_date: int,
    name_test: str,
    teacher_id: int,
):
    get_progress = await async_client.get(
        f"{settings.api_v1_prefix}/tests/{test_id}/progress_test"
    )
    assert get_progress.status_code == 200
    data = get_progress.json()
    assert data["test_id"] == test_id
    assert data["status"] == status
    assert data["deadline_date"] == deadline_date
    assert data["test"]["name"] == name_test
    assert data["test"]["creator_id"] == teacher_id


async def get_progress_test_complete(
    async_client,
    test_id: int,
    count_current_answer: int,
):
    get_progress = await async_client.get(
        f"{settings.api_v1_prefix}/tests/{test_id}/progress_test"
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


async def start_test_test(
    async_client,
    test_id: int,
):
    start_test = await async_client.post(
        f"{settings.api_v1_prefix}/tests/{test_id}/start_test"
    )
    assert start_test.status_code == 200


async def completion_test(
    async_client, test_id: int, result_test: List[QuestionResultBase]
):
    completion = await async_client.post(
        f"{settings.api_v1_prefix}/tests/{test_id}/completion_test", json=result_test
    )
    assert completion.status_code == 200


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
