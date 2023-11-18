"""Add is_active column to User model

Revision ID: 520d945a0312
Revises: 0a566f2abfaa
Create Date: 2023-09-03 00:36:15.157611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '520d945a0312'
down_revision = '0a566f2abfaa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
