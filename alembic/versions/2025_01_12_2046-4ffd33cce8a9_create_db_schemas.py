"""create db schemas

Revision ID: 4ffd33cce8a9
Revises: 
Create Date: 2025-01-12 20:46:43.485661

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4ffd33cce8a9"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "question",
        sa.Column("text_question", sa.String(), nullable=False),
        sa.Column("options", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("correct_answer", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "role",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "profile",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("gender", sa.Integer(), nullable=True),
        sa.Column("role_id", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "course",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
        sa.Column("teacher_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["teacher_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("time_limit", sa.Integer(), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "user",
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("profile_id"),
    )
    op.create_table(
        "course_student_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("profile_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["profile_id"],
            ["profile.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "course_test_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("course_id", sa.Integer(), nullable=False),
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["course_id"],
            ["course.id"],
        ),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test_progress",
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.Column("participant_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("status", sa.Integer(), nullable=True),
        sa.Column("deadline_date", sa.Integer(), nullable=True),
        sa.Column("attempt_date", sa.Integer(), nullable=True),
        sa.Column("timelimit", sa.Integer(), nullable=True),
        sa.Column("count_current_answer", sa.Integer(), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["profile.id"],
        ),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test_question_association",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("test_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["question.id"],
        ),
        sa.ForeignKeyConstraint(
            ["test_id"],
            ["test.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "test_progress_result",
        sa.Column("test_progress_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("text_question", sa.String(), nullable=False),
        sa.Column("options", sa.ARRAY(sa.String()), nullable=False),
        sa.Column("correct_answer", sa.String(), nullable=False),
        sa.Column("student_answer", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["test_progress_id"],
            ["test_progress.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("test_progress_result")
    op.drop_table("test_question_association")
    op.drop_table("test_progress")
    op.drop_table("course_test_association")
    op.drop_table("course_student_association")
    op.drop_table("user")
    op.drop_table("test")
    op.drop_table("course")
    op.drop_table("profile")
    op.drop_table("role")
    op.drop_table("question")
    # ### end Alembic commands ###
