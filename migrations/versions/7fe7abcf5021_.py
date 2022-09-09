"""empty message

Revision ID: 7fe7abcf5021
Revises: 2849f5f705ed
Create Date: 2022-09-09 18:14:41.406983

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fe7abcf5021'
down_revision = '2849f5f705ed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parsingtask', sa.Column('parsing_type', sa.Enum('AA', 'NA', 'AA+NA', name='parsingtype'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parsingtask', 'parsing_type')
    # ### end Alembic commands ###
