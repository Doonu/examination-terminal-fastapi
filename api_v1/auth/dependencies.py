import datetime
from datetime import timedelta
from typing import Optional

import pytz
from fastapi import Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.auth import crud as auth_crud
from api_v1.auth.helpers import (
    validate_token_type,
    TOKEN_TYPE_FIELD,
    REFRESH_TOKEN_TYPE,
    ACCESS_TOKEN_TYPE,
)
from api_v1.auth.schemas import AuthBase
from api_v1.auth.utils import hash_password, validate_password, encode_jwt, decode_jwt
from api_v1.profile import crud as profile_crud, crud
from core.config import settings
from core.models import User, db_helper


http_bearer = HTTPBearer()


async def create_tokens_by_auth(user: User, session: AsyncSession):
    access_token = await create_access_token(user=user, session=session)
    refresh_token = await create_refresh_token(user=user)
    return AuthBase(
        token_type="Bearer", refresh_token=refresh_token, access_token=access_token
    )


async def create_token(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


async def register_user(
    email: EmailStr = Form(),
    role_id: int = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    existing_user = await auth_crud.get_user_by_email(email=email, session=session)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists",
        )

    base_role = await auth_crud.get_role_by_id(session=session, role_id=role_id)
    profile = await profile_crud.create_profile(
        session=session, email=email, role_id=base_role.id
    )

    hashed_password = hash_password(password_user=password)
    return await auth_crud.create_user(
        session=session,
        hashed_password=hashed_password,
        email=email,
        profile_id=profile.id,
    )


async def validate_auth_user(
    user: User = Depends(auth_crud.get_user_by_email), password: str = Form()
):
    authed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверный логин или пароль"
    )

    if not user:
        raise authed_exc

    if not validate_password(password_user=password, hashed_password=user.password):
        raise authed_exc

    return user


async def get_current_token_payload(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> User:
    token = credentials.credentials
    payload = decode_jwt(token=token)
    return payload


async def get_user_id_in_access_token(
    payload: dict = Depends(get_current_token_payload),
) -> int:
    return payload.get("user_id")


async def get_current_auth_user_for_refresh(
    payload: dict = Depends(get_current_token_payload),
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
) -> User:
    validate_token_type(token_type=REFRESH_TOKEN_TYPE, payload=payload)
    user_id = await get_user_id_in_access_token(payload=payload)
    user = await auth_crud.get_item_user_by_id(session=session, user_id=user_id)

    if user is not None:
        return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="token not found"
    )


async def create_access_token(user: User, session: AsyncSession) -> str:
    profile = await crud.get_profile(session=session, user_id=user.id)
    jwt_payload = {
        "email": user.email,
        "user_id": user.id,
        "sub": user.email,
        "role_id": profile.role_id,
    }
    return await create_token(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth.access_token_expire_minutes,
    )


async def create_refresh_token(user: User) -> str:
    jwt_payload = {"sub": user.email, "user_id": user.id}
    return await create_token(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.auth.refresh_token_expire_days,
    )
