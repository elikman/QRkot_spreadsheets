"""Add user field in Donation model

Revision ID: 935be8bd95d2
Revises: 59ee8fd8ec6b
Create Date: 2024-09-13 20:52:28.868874

"""

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "935be8bd95d2"
down_revision = "59ee8fd8ec6b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("donation", schema=None) as batch_op:
        batch_op.add_column(sa.Column("user_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key(
            "fk_donation_user_id_user", "user", ["user_id"], ["id"]
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("donation", schema=None) as batch_op:
        batch_op.drop_constraint("fk_donation_user_id_user", type_="foreignkey")
        batch_op.drop_column("user_id")

    # ### end Alembic commands ###
