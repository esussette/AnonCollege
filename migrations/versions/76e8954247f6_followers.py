"""followers

Revision ID: 76e8954247f6
Revises: 724fbce33975
Create Date: 2020-12-15 15:33:27.454576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e8954247f6'
down_revision = '724fbce33975'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('followers',
    sa.Column('follower_id', sa.Integer(), nullable=True),
    sa.Column('followed_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['followed_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['follower_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    # ### end Alembic commands ###
