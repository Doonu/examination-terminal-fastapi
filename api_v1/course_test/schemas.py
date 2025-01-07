from pydantic import BaseModel, ConfigDict

from api_v1.profile.schemas import ProfileGet


class TestBase(BaseModel):
    name: str
    time_limit: int
    creator_id: int
    creator: ProfileGet


class Test(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
