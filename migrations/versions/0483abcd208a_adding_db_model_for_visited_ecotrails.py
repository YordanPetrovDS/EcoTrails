"""Adding DB Model for visited ecotrails

Revision ID: 0483abcd208a
Revises: a1c6cae77bed
Create Date: 2022-01-09 20:35:03.199384

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0483abcd208a'
down_revision = 'a1c6cae77bed'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('ecotrails_planned',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('photo_url', sa.String(length=255), nullable=False),
    sa.Column('area', sa.String(length=255), nullable=False),
    sa.Column('mountain', sa.String(length=255), nullable=False),
    sa.Column('length', sa.Float(), nullable=False),
    sa.Column('denivelation', sa.Integer(), nullable=True),
    sa.Column('difficulty', sa.Integer(), nullable=False),
    sa.Column('create_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('ecotrails_planned')
    # ### end Alembic commands ###