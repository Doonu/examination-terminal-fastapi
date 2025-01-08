from typing import List, Optional

from pydantic import BaseModel, ConfigDict, field_validator


class QuestionBase(BaseModel):
    text_question: str
    options: List[str]
    correct_answer: str


class Question(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class QuestionGet(QuestionBase):
    pass
