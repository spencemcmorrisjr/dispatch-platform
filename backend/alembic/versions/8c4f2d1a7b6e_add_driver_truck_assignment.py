"""add driver truck assignment and company name

Revision ID: 8c4f2d1a7b6e
Revises: 4773d564f20e
Create Date: 2026-09-30
"""

from alembic import op
import sqlalchemy as sa


revision = "8c4f2d1a7b6e"
down_revision = "4773d564f20e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("drivers") as batch_op:
        batch_op.add_column(
            sa.Column("company_name", sa.String(), nullable=True)
        )

    with op.batch_alter_table("trucks") as batch_op:
        batch_op.create_foreign_key(
            "fk_trucks_driver_id_drivers",
            "drivers",
            ["driver_id"],
            ["id"],
            ondelete="SET NULL",
        )


def downgrade():
    with op.batch_alter_table("trucks") as batch_op:
        batch_op.drop_constraint(
            "fk_trucks_driver_id_drivers",
            type_="foreignkey",
        )

    with op.batch_alter_table("drivers") as batch_op:
        batch_op.drop_column("company_name")
