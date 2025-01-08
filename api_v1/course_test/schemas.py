from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from api_v1.profile.schemas import ProfileGet
from api_v1.questions.schemas import QuestionGet


class TestBase(BaseModel):
    name: str
    time_limit: int
    creator_id: int
    creator: ProfileGet


class Test(TestBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TestGet(Test):
    questions: Optional[list[QuestionGet]] = []

    @field_validator("questions", mode="before")
    @classmethod
    def flatten_students(cls, value):
        if not value:
            return []
        return [assoc.question for assoc in value]
