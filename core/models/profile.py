from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import User
    from .role import Role


class Profile(Base):
    email: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)
    gender: Mapped[int] = mapped_column(
        Integer, CheckConstraint("gender IN (1, 2)"), nullable=True
    )

    role_id: Mapped[int] = mapped_column(ForeignKey("role.id"), nullable=True)
    role: Mapped["Role"] = relationship("Role", lazy="joined")

    user: Mapped["User"] = relationship(back_populates="profile")

