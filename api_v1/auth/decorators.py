from functools import wraps
from typing import Callable

from fastapi import HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth.dependencies import get_current_token_payload
from api_v1.role import crud
from core.models import db_helper


http_bearer = HTTPBearer()


def role_required(role_name: str):
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(
            *args,
            **kwargs,
        ):
            request = kwargs.get("request")
            if request is None:
                for arg in args:
                    if isinstance(arg, Request):
                        request = arg
                        break

            if request is None:
                raise RuntimeError(
                    "Объект 'request' не найден в аргументах функции, "
                    "укажите параметр 'request: Request' в сигнатуре обработчика."
                )

            credentials: HTTPAuthorizationCredentials = await http_bearer(request)

            payload = await get_current_token_payload(credentials=credentials)
            session_gen = db_helper.scoped_session_dependency()
            session: AsyncSession = await session_gen.__anext__()

            role_id = payload.get("role_id")

            if role_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Role ID is missing in the token",
                )

            role_list = await crud.get_role_list(session=session)
            expected_role = next(
                (role for role in role_list if role.name == role_name), None
            )

            if expected_role is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Invalid role name: {role_name}",
                )
            if role_id != expected_role.id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access forbidden for role {role_name}",
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
