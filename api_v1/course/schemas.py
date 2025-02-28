from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from api_v1.course_test.schemas import Test, TestInCourse
from api_v1.profile.schemas import ProfileGet


class CourseBase(BaseModel):
    id: int
    name: str
    description: str
    teacher_id: int
    teacher: ProfileGet


class Course(CourseBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CourseGet(Course):
    students: Optional[list[ProfileGet]]
    tests: Optional[list[Test]]

    @field_validator("students", mode="before")
    @classmethod
    def flatten_students(cls, value):
        if not value:
            return []
        return [assoc.student for assoc in value]

    @field_validator("tests", mode="before")
    @classmethod
    def flatten_tests(cls, value):
        if not value:
            return []
        return [assoc.test for assoc in value]


class CourseItemGet(CourseGet):
    tests: Optional[list[TestInCourse]]


class CourseUpdatePartial(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
