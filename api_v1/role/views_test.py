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
