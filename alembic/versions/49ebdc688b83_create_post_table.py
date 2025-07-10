"""add user table

Revision ID: 49ebdc688b83
Revises: ebfa2039d262
Create Date: 2025-07-10 15:25:47.011761

"""
from typing import Sequence, Union 
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49ebdc688b83'
down_revision: Union[str, Sequence[str], None] = 'ebfa2039d262'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
