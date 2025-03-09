"""fix latitude longitude types

Revision ID: 4399b33d8125
Revises: de769b0776bc
Create Date: 2025-03-09 15:26:33.629166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4399b33d8125'
down_revision: Union[str, None] = 'de769b0776bc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('location', 'latitude',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=8),
               existing_nullable=False)
    op.alter_column('location', 'longitude',
               existing_type=sa.REAL(),
               type_=sa.Numeric(precision=8),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('location', 'longitude',
               existing_type=sa.Numeric(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    op.alter_column('location', 'latitude',
               existing_type=sa.Numeric(precision=8),
               type_=sa.REAL(),
               existing_nullable=False)
    # ### end Alembic commands ###
