"""сÐcreate test_progress

Revision ID: 200a898f0c9f
Revises: 012074672316
Create Date: 2025-01-12 14:12:10.358193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "200a898f0c9f"
down_revision: Union[str, None] = "012074672316"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Обновляем столбец deadline_date: преобразуем TIMESTAMP в INTEGER используя Unix timestamp
    op.alter_column(
        "test_progress",
        "deadline_date",
        existing_type=postgresql.TIMESTAMP(),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="EXTRACT(EPOCH FROM deadline_date)::integer",
    )
    # Аналогично для timelimit, если хотите сохранить интервал в виде количества секунд (целое число)
    op.alter_column(
        "test_progress",
        "timelimit",
        existing_type=postgresql.INTERVAL(),
        type_=sa.Integer(),
        existing_nullable=True,
        postgresql_using="EXTRACT(EPOCH FROM timelimit)::integer",
    )


def downgrade() -> None:
    # При откате преобразовываем INTEGER обратно в TIMESTAMP для deadline_date
    op.alter_column(
        "test_progress",
        "deadline_date",
        existing_type=sa.Integer(),
        type_=postgresql.TIMESTAMP(),
        existing_nullable=True,
        postgresql_using="to_timestamp(deadline_date)",
    )
    # Аналогично для timelimit - преобразуем обратно в INTERVAL
    op.alter_column(
        "test_progress",
        "timelimit",
        existing_type=sa.Integer(),
        type_=postgresql.INTERVAL(),
        existing_nullable=True,
        postgresql_using="make_interval(secs => timelimit)",
    )
