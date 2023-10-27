"""bugfix

Revision ID: 9cf01d3100d7
Revises: 7f0351f9271c
Create Date: 2023-03-15 06:26:04.489798

"""
from alembic import op
import sqlalchemy as sa
import citext


# revision identifiers, used by Alembic.
revision = '9cf01d3100d7'
down_revision = '7f0351f9271c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
