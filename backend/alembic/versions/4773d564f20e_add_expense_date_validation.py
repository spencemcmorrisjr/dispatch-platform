from alembic import op
import sqlalchemy as sa


revision = "4773d564f20e"
down_revision = "9cb271723c86"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "expense_date",
            existing_type=sa.String(),
            type_=sa.Date(),
            existing_nullable=False,
        )


def downgrade():
    with op.batch_alter_table("expenses") as batch_op:
        batch_op.alter_column(
            "expense_date",
            existing_type=sa.Date(),
            type_=sa.String(),
            existing_nullable=False,
        )
