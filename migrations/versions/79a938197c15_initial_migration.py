"""initial migration

Revision ID: 79a938197c15
Revises: 
Create Date: 2024-12-09 05:17:55.562922

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '79a938197c15'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candle',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('price', sa.Float(), nullable=False),
    sa.Column('stock', sa.Integer(), nullable=False),
    sa.Column('image_filename', sa.String(length=255), nullable=True),
    sa.Column('image_reference', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('address',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('address_line1', sa.String(length=255), nullable=False),
    sa.Column('address_line2', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=100), nullable=True),
    sa.Column('postal_code', sa.String(length=20), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('basket',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('candle_category',
    sa.Column('candle_id', sa.Integer(), nullable=False),
    sa.Column('category_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candle_id'], ['candle.id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.PrimaryKeyConstraint('candle_id', 'category_id')
    )
    op.create_table('basket_candle',
    sa.Column('basket_id', sa.Integer(), nullable=False),
    sa.Column('candle_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['basket_id'], ['basket.id'], ),
    sa.ForeignKeyConstraint(['candle_id'], ['candle.id'], ),
    sa.PrimaryKeyConstraint('basket_id', 'candle_id')
    )
    op.create_table('basket_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('basket_id', sa.Integer(), nullable=False),
    sa.Column('candle_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['basket_id'], ['basket.id'], ),
    sa.ForeignKeyConstraint(['candle_id'], ['candle.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('order_date', sa.DateTime(), nullable=False),
    sa.Column('total_price', sa.Float(), nullable=False),
    sa.Column('delivery_address_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['delivery_address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_item',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('candle_id', sa.Integer(), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['candle_id'], ['candle.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_item')
    op.drop_table('order')
    op.drop_table('basket_item')
    op.drop_table('basket_candle')
    op.drop_table('candle_category')
    op.drop_table('basket')
    op.drop_table('address')
    op.drop_table('user')
    op.drop_table('category')
    op.drop_table('candle')
    # ### end Alembic commands ###
