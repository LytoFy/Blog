"""empty message

Revision ID: ca4d174875a7
Revises: a224bea1087f
Create Date: 2019-08-30 19:41:42.802124

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ca4d174875a7'
down_revision = 'a224bea1087f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('father', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'father')
    # ### end Alembic commands ###
