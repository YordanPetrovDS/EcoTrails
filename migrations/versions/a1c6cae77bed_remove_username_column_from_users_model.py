"""remove username column from users model

Revision ID: a1c6cae77bed
Revises: 426526dd64c2
Create Date: 2022-01-02 18:13:58.977458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1c6cae77bed'
down_revision = '426526dd64c2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('administrators', 'username')
    op.drop_column('moderators', 'username')
    op.drop_column('users', 'username')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('moderators', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('administrators', sa.Column('username', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
