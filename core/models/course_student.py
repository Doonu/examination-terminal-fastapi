from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import TYPE_CHECKING
from core.models import Base


if TYPE_CHECKING:
    from .profile import Profile
    from .course import Course


class CourseStudentAssociation(Base):
    __tablename__ = "course_student_association"
    __table_args = UniqueConstraint(
        "course_id", "profile_id", name="id_unique_course_profile"
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profile.id"))

    student: Mapped["Profile"] = relationship(back_populates="courses")
    course: Mapped["Course"] = relationship(back_populates="students")
