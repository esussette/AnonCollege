"""empty message

Revision ID: 5dba83a29e5c
Revises: 0f9e529f23a0
Create Date: 2020-12-15 01:40:42.569012

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5dba83a29e5c'
down_revision = '0f9e529f23a0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('title', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'title')
    # ### end Alembic commands ###
