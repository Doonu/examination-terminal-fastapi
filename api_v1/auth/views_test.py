from core.config import settings


async def registration_test(async_client, email: str, role_id: int, password: str):
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


async def auth_login_test(async_client, email: str, password: str):
    session = await async_client.post(
        f"{settings.api_v1_prefix}/auth/login",
        data={"email": email, "password": password},
    )
    assert session.status_code == 200
    data = session.json()
    access_token = data.get("access_token")

    async_client.headers.update({"Authorization": f"Bearer {access_token}"})
