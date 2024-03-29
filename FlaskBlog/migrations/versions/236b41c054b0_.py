"""empty message

Revision ID: 236b41c054b0
Revises: d01860e1b346
Create Date: 2019-08-31 10:02:49.774309

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '236b41c054b0'
down_revision = 'd01860e1b346'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('b', sa.DateTime(), nullable=True))
    op.drop_column('comments', 'a')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('a', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('comments', 'b')
    # ### end Alembic commands ###
