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
