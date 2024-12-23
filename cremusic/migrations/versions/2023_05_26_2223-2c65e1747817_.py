"""empty message

Revision ID: 2c65e1747817
Revises: 
Create Date: 2023-05-26 22:23:29.447624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c65e1747817'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('book',
    sa.Column('type', sa.String(length=32), nullable=True),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('background_image_url', sa.String(length=1024), nullable=True),
    sa.Column('background_color_code', sa.SmallInteger(), nullable=True),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.String(length=256), server_default='system', nullable=False),
    sa.Column('modified_by', sa.String(length=256), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('config',
    sa.Column('required_unlock', sa.Boolean(), nullable=True),
    sa.Column('global_code', sa.String(length=250), nullable=True),
    sa.Column('secret', sa.String(length=250), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statistic_log',
    sa.Column('name', sa.String(length=256), nullable=False),
    sa.Column('code', sa.String(length=64), nullable=False),
    sa.Column('telephone', sa.String(length=16), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('telephone', 'code')
    )
    op.create_table('book_code',
    sa.Column('serial', sa.String(length=64), nullable=False),
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.Column('code', sa.String(length=64), nullable=False),
    sa.Column('release_version', sa.String(length=64), nullable=False),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('code'),
    sa.UniqueConstraint('serial')
    )
    op.create_table('book_episode',
    sa.Column('book_id', sa.BigInteger(), nullable=False),
    sa.Column('name', sa.String(length=256), nullable=True),
    sa.Column('author', sa.String(length=256), server_default='', nullable=True),
    sa.Column('artist', sa.String(length=256), server_default='', nullable=True),
    sa.Column('background_image_url', sa.String(length=1024), nullable=True),
    sa.Column('background_color_code', sa.Integer(), nullable=True),
    sa.Column('created_by', sa.String(length=128), server_default='system', nullable=False),
    sa.Column('created_date', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('modified_by', sa.String(length=128), nullable=True),
    sa.Column('modified_date', sa.DateTime(), nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_id'], ['book.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('book_episode_video',
    sa.Column('book_episode_id', sa.BigInteger(), nullable=False),
    sa.Column('video_id', sa.String(length=64), nullable=False),
    sa.Column('name', sa.String(length=1024), nullable=True),
    sa.Column('link', sa.String(length=1024), nullable=True),
    sa.Column('thumbnail', sa.String(length=1024), nullable=True),
    sa.Column('duration', sa.BigInteger(), server_default='0', nullable=True),
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.ForeignKeyConstraint(['book_episode_id'], ['book_episode.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('book_episode_video')
    op.drop_table('book_episode')
    op.drop_table('book_code')
    op.drop_table('statistic_log')
    op.drop_table('config')
    op.drop_table('book')
    # ### end Alembic commands ###
