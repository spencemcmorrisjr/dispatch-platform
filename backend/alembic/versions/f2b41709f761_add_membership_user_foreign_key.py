"""add membership user foreign key"""

from alembic import op

revision = "f2b41709f761"
down_revision = "8c4f2d1a7b6e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("business_memberships") as batch_op:
        batch_op.create_foreign_key(
            "fk_business_memberships_user_id_users",
            "users",
            ["user_id"],
            ["id"],
        )


def downgrade():
    with op.batch_alter_table("business_memberships") as batch_op:
        batch_op.drop_constraint(
            "fk_business_memberships_user_id_users",
            type_="foreignkey",
        )
