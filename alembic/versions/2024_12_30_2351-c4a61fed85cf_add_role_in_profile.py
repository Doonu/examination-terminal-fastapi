"""add role in profile

Revision ID: c4a61fed85cf
Revises: 09a76cd4cd15
Create Date: 2024-12-30 23:51:33.965692

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c4a61fed85cf"
down_revision: Union[str, None] = "09a76cd4cd15"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("profile", sa.Column("role_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "profile", "role", ["role_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "profile", type_="foreignkey")
    op.drop_column("profile", "role_id")
    # ### end Alembic commands ###
