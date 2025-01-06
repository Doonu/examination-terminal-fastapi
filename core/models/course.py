from typing import TYPE_CHECKING
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base


if TYPE_CHECKING:
    from .profile import Profile
    from .course_student import CourseStudentAssociation


class Course(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)

    teacher_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False)
    teacher: Mapped["Profile"] = relationship("Profile", lazy="joined")

    students: Mapped[list["CourseStudentAssociation"]] = relationship(
        back_populates="course"
    )
