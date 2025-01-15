from core.config import settings


async def get_profile_test(async_client, email: str, profile_id: int):
    profile = await async_client.get(f"{settings.api_v1_prefix}/profile/me")
    assert profile.status_code == 200
    data = profile.json()
    assert data["email"] == email
    assert data["id"] == profile_id
