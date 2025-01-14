from typing import List

import pytest
from pydantic import EmailStr

from core.config import settings


async def create_role_test(async_client, role_id: int, name: str):
    role = await async_client.post(
        f"{settings.api_v1_prefix}/role/", data={"role_name": name}
    )
    assert role.status_code == 200, role.text
    data = role.json()
    assert data["id"] == role_id
    assert data["name"] == name


async def get_role_list_test(async_client, role_list):
    role = await async_client.get(f"{settings.api_v1_prefix}/role/")
    assert role.status_code == 200, role.text
    data = role.json()
    assert data == role_list


async def registration_test(async_client, email: EmailStr, role_id: int, password: str):
    session = await async_client.post(
        f"{settings.api_v1_prefix}/auth/registration",
        data={
            "email": email,
            "role_id": role_id,
            "password": password,
        },
    )
    assert session.status_code == 200
    data = session.json()
    access_token = data.get("access_token")
    assert access_token, "Access token не найден"

    async_client.headers.update({"Authorization": f"Bearer {access_token}"})


async def get_profile_test(async_client, email: EmailStr, profile_id: int):
    profile = await async_client.get(f"{settings.api_v1_prefix}/profile/me")
    assert profile.status_code == 200
    data = profile.json()
    assert data["email"] == email
    assert data["id"] == profile_id


async def create_course_test(async_client, name: str, description: str):
    created_course = await async_client.post(
        f"{settings.api_v1_prefix}/course/",
        data={"name": name, "description": description},
    )
    assert created_course.status_code == 200


# Допилить с массивами students и tests
async def get_course_test(
    async_client, course_id: int, name: str, description: str, teacher_id: int
):
    course_list = await async_client.get(f"{settings.api_v1_prefix}/course/{course_id}")
    assert course_list.status_code == 200
    data = course_list.json()
    assert data["id"] == course_id
    assert data["name"] == name
    assert data["description"] == description
    assert data["teacher_id"] == teacher_id


async def create_test_item_test(async_client, name: str, time_limit: int):
    item_test = await async_client.post(
        f"{settings.api_v1_prefix}/tests/",
        data={"name_test": name, "time_limit": time_limit},
    )
    assert item_test.status_code == 200


async def add_test_in_course_test(async_client, course_id: int, test_ids: List[int]):
    test_in_course = await async_client.post(
        f"{settings.api_v1_prefix}/course/{course_id}/add_test",
        json=test_ids,
    )
    assert test_in_course.status_code == 200


role_teacher = "Преподаватель"
role_teacher_id = 1
role_student = "Студент"
role_student_id = 2

email_teacher = "teacher@mail.ru"
password_teacher = "qwerty"
id_teacher = 1

email_student = "student@mail.ru"
password_student = "qwerty"
id_student = 2


name_course = "Математика"
description_course = "Базовая математика"
id_course = 1

name_test = "Математика тест 1"
limit = 3600
id_test = 1


@pytest.mark.asyncio
async def test_course_test(async_client):
    await get_role_list_test(async_client, role_list=[])
    await create_role_test(async_client, role_id=1, name=role_teacher)
    await create_role_test(async_client, role_id=2, name=role_student)
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
    await add_test_in_course_test(async_client, course_id=id_course, test_ids=[id_test])

    await get_course_test(
        async_client,
        course_id=id_course,
        name=name_course,
        description=description_course,
        teacher_id=id_teacher,
    )
