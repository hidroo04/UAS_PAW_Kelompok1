"""add payments table

Revision ID: 003
Revises: 002
Create Date: 2025-12-18

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002_add_enhancements'
branch_labels = None
depends_on = None


def upgrade():
    # Create payments table
    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('member_id', sa.Integer(), nullable=False),
        sa.Column('order_id', sa.String(100), nullable=False),
        sa.Column('amount', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_method', sa.String(50), nullable=True),
        sa.Column('status', sa.String(20), server_default='pending'),
        sa.Column('membership_plan', sa.String(50), nullable=False),
        sa.Column('duration_days', sa.Integer(), server_default='30'),
        sa.Column('transaction_id', sa.String(100), nullable=True),
        sa.Column('payment_url', sa.String(500), nullable=True),
        sa.Column('va_number', sa.String(50), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now()),
        sa.Column('paid_at', sa.DateTime(), nullable=True),
        sa.Column('expired_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['member_id'], ['members.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_id')
    )
    
    # Create index on order_id for faster lookups
    op.create_index('ix_payments_order_id', 'payments', ['order_id'])
    op.create_index('ix_payments_member_id', 'payments', ['member_id'])
    op.create_index('ix_payments_status', 'payments', ['status'])


def downgrade():
    op.drop_index('ix_payments_status', 'payments')
    op.drop_index('ix_payments_member_id', 'payments')
    op.drop_index('ix_payments_order_id', 'payments')
    op.drop_table('payments')
