"""empty message

Revision ID: 187011c62597
Revises: ccff17983614
Create Date: 2019-08-31 10:03:38.558100

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '187011c62597'
down_revision = 'ccff17983614'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'date')
    # ### end Alembic commands ###
