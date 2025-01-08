from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class QuestionBase(BaseModel):
    text_question: str
    options: List[str]
    correct_answer: str


class Question(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class QuestionGet(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class QuestionUpdatePartial(BaseModel):
    text_question: Optional[str] = None
    options: Optional[List[str]] = []
    correct_answer: Optional[str] = None
