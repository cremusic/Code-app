"""modified_by_nullable

Revision ID: cb16919f71c4
Revises: 70981ff17fee
Create Date: 2023-05-22 23:04:27.507453

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb16919f71c4'
down_revision = '70981ff17fee'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book', 'modified_by',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.alter_column('book_episode', 'modified_by',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('book_episode', 'modified_by',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.alter_column('book', 'modified_by',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    # ### end Alembic commands ###
