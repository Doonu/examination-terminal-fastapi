from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict

from api_v1.role.schemas import Role


class ProfileBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = Field(
        None, description="Пол: 2 - мужской, 1 - женский", ge=1, le=2
    )


class Profile(ProfileBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class ProfileUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[int] = Field(
        None, description="Пол: 2 - мужской, 1 - женский", ge=1, le=2
    )


class ProfileGet(Profile):
    role: Role
    role_id: int
