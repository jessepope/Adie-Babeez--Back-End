"""empty message

Revision ID: 5bc79a4086b4
Revises: c1b1747e4bda
Create Date: 2022-02-09 12:35:12.783139

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bc79a4086b4'
down_revision = 'c1b1747e4bda'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_id_chatengine', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_id_chatengine')
    # ### end Alembic commands ###
