"""баланс100

Revision ID: 07717113a796
Revises: 2fcfa98e0ba9
Create Date: 2025-01-17 11:35:35.885364

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "07717113a796"
down_revision: Union[str, None] = "2fcfa98e0ba9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('users', 'balance',
                    server_default=sa.text('100'),
                    existing_type=sa.Integer())

def downgrade():
    op.alter_column('users', 'balance',
                    server_default=sa.text('0'), 
                    existing_type=sa.Integer())
