from datetime import timedelta, datetime
from typing import Optional

import bcrypt
import jwt
from fastapi import HTTPException, status

from core.config import settings


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth.private_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
    expire_minutes: int = settings.auth.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
):
    to_encode = payload.copy()
    now = datetime.utcnow()

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(

    token: str,
    public_key: str = settings.auth.public_key_path.read_text(),
    algorithm: str = settings.auth.algorithm,
):
    try:
        decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Token has expired"
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token"
        )


def hash_password(password_user: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes: bytes = password_user.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password_user: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=password_user.encode(), hashed_password=hashed_password
    )
