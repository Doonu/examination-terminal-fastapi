from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .course_test import CourseTestAssociation
    from .profile import Profile


class Test(Base):
    name: Mapped[str] = mapped_column(String, nullable=False)
    time_limit: Mapped[int] = mapped_column(Integer, nullable=False)

    creator_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=False)
    creator: Mapped["Profile"] = relationship("Profile", lazy="joined")

    courses: Mapped[list["CourseTestAssociation"]] = relationship(back_populates="test")
