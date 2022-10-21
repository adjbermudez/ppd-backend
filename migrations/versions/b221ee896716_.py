"""empty message

Revision ID: b221ee896716
Revises: 
Create Date: 2022-10-20 23:32:15.049961

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b221ee896716'
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
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=250), nullable=False),
    sa.Column('subtitle', sa.Text(), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('highlighted', sa.Text(), nullable=False),
    sa.Column('complete', sa.Text(), nullable=False),
    sa.Column('image', sa.String(length=200), nullable=False),
    sa.Column('image_secondary', sa.String(length=200), nullable=True),
    sa.Column('image_preview', sa.String(length=200), nullable=False),
    sa.Column('public_id_image', sa.String(length=100), nullable=False),
    sa.Column('public_id_secondary', sa.String(length=100), nullable=False),
    sa.Column('public_id_preview', sa.String(length=100), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('unore',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('update_at', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('unore')
    op.drop_table('news')
    op.drop_table('user')
    # ### end Alembic commands ###
