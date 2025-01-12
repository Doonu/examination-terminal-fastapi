from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List

from sqlalchemy import (
    Integer,
    CheckConstraint,
    func,
    DateTime,
    Interval,
    String,
    ARRAY,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from .test import Test
    from .profile import Profile

# status:
# 1 - готов для прохождения
# 2 - начат
# 3 - закончен
# 4 - просрочено по времени


class TestProgress(Base):
    __tablename__ = "test_progress"
    test_id: Mapped[int] = mapped_column(ForeignKey("test.id"), nullable=False)
    test: Mapped["Test"] = relationship("Test", lazy="joined")

    participant_id: Mapped[int] = mapped_column(ForeignKey("profile.id"), nullable=True)
    participant: Mapped["Profile"] = relationship("Profile", lazy="joined")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), default=datetime.now
    )
    status: Mapped[int] = mapped_column(
        Integer, CheckConstraint("status IN (1, 2, 3, 4)"), nullable=True
    )
    deadline_date: Mapped[int] = mapped_column(Integer, nullable=True)
    attempt_date: Mapped[int] = mapped_column(Integer, nullable=True)
    timelimit: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
    )
    count_current_answer: Mapped[int] = mapped_column(Integer, nullable=True)
    result_test: Mapped[List["TestProgressResult"]] = relationship(
        "TestProgressResult", back_populates="test_progress"
    )


class TestProgressResult(Base):
    __tablename__ = "test_progress_result"
    test_progress_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("test_progress.id"), nullable=False
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text_question: Mapped[str] = mapped_column(String, nullable=False)
    options: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    correct_answer: Mapped[str] = mapped_column(String, nullable=False)
    student_answer: Mapped[str] = mapped_column(String, nullable=True)

    test_progress: Mapped["TestProgress"] = relationship(
        "TestProgress", back_populates="result_test"
    )
