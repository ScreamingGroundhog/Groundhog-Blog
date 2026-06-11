"""add blog_description to user

Revision ID: f8a7b3c2d1e6
Revises: 9ac93e768062
Create Date: 2026-06-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8a7b3c2d1e6'
down_revision = '9ac93e768062'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('blog_description', sa.String(length=512), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('blog_description')
