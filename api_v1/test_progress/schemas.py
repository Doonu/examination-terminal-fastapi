from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from api_v1.course_test.schemas import Test


class TestProgressResultTest(BaseModel):
    id: int
    text_question: str
    options: List[str]
    correct_answer: str
    student_answer: Optional[str]


class TestProgressTest(BaseModel):
    id: int
    participant_id: int
    test_id: int
    status: int
    attempt_date: Optional[int]
    count_current_answer: Optional[int]
    created_at: datetime
    deadline_date: int
    timelimit: int
    test: Test
    result_test: List[TestProgressResultTest]
    remaining_time: Optional[int] = None
