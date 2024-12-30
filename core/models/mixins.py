from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .profile import Profile


class ProfileRelationMixin:
    _profile_id_unique: bool = False
    _profile_back_populates: Optional[str] = None
    _profile_id_nullable: bool = False

    @declared_attr
    def profile_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey("profile.id"),
            unique=cls._profile_id_unique,
            nullable=cls._profile_id_nullable,
        )

    @declared_attr
    def profile(cls) -> Mapped["Profile"]:
        return relationship("Profile", back_populates=cls._profile_back_populates)
