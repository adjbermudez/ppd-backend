"""empty message

Revision ID: c302bb94a6d0
Revises: 
Create Date: 2022-08-29 21:32:59.201555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c302bb94a6d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=80), nullable=False),
    sa.Column('fullname', sa.String(length=80), nullable=False),
    sa.Column('password', sa.String(length=250), nullable=False),
    sa.Column('salt', sa.String(length=120), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('rol', sa.Enum('ADMINISTRATOR', 'GENERAL', name='userrol'), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'DISABLED', 'DELETE', name='userstatus'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
