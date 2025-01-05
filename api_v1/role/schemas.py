from pydantic import BaseModel, ConfigDict


class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
