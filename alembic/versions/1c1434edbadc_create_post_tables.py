"""create post tables

Revision ID: 1c1434edbadc
Revises: 
Create Date: 2023-07-21 13:43:12.298814

"""
from alembic import op
import sqlalchemy as sa

#10:51:38
# revision identifiers, used by Alembic.
revision = '1c1434edbadc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts6', sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True))
    pass


def downgrade() -> None:
    op.drop_table('posts6')
    pass
