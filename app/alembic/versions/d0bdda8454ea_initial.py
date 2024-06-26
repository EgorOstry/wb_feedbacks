"""Initial

Revision ID: d0bdda8454ea
Revises: 
Create Date: 2024-02-13 22:37:22.316328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0bdda8454ea'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('products_mapping',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('marketplace_id', sa.Integer(), nullable=True),
    sa.Column('internal_code', sa.String(), nullable=True),
    sa.Column('external_code', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('external_code')
    )
    op.create_table('product_details',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('imt_id', sa.Integer(), nullable=True),
    sa.Column('nmId', sa.Integer(), nullable=True),
    sa.Column('product_name', sa.String(), nullable=True),
    sa.Column('supplier_article', sa.String(), nullable=True),
    sa.Column('supplier_name', sa.String(), nullable=True),
    sa.Column('brand_name', sa.String(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['nmId'], ['products_mapping.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('text', sa.String(), nullable=True),
    sa.Column('product_valuation', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.Column('answer', sa.String(), nullable=True),
    sa.Column('state', sa.String(), nullable=True),
    sa.Column('video', sa.String(), nullable=True),
    sa.Column('was_viewed', sa.Boolean(), nullable=True),
    sa.Column('photo_links', sa.String(), nullable=True),
    sa.Column('user_name', sa.String(), nullable=True),
    sa.Column('matching_size', sa.String(), nullable=True),
    sa.Column('is_able_supplier_feedback_valuation', sa.Boolean(), nullable=True),
    sa.Column('supplier_feedback_valuation', sa.Integer(), nullable=True),
    sa.Column('is_able_supplier_product_valuation', sa.Boolean(), nullable=True),
    sa.Column('supplier_product_valuation', sa.Integer(), nullable=True),
    sa.Column('is_able_return_product_orders', sa.Boolean(), nullable=True),
    sa.Column('return_product_orders_date', sa.DateTime(), nullable=True),
    sa.Column('bables', sa.String(), nullable=True),
    sa.Column('product_detail_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_detail_id'], ['product_details.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('feedbacks')
    op.drop_table('product_details')
    op.drop_table('products_mapping')
    # ### end Alembic commands ###
