"""add user profile table

Revision ID: 003
Revises: 002
Create Date: 2025-12-17

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade():
    # Tambahkan kolom phone ke tabel users
    op.add_column('users', sa.Column('phone', sa.String(20), nullable=True))
    
    # Tambahkan kolom address ke tabel users
    op.add_column('users', sa.Column('address', sa.Text, nullable=True))
    
    # Tambahkan kolom avatar_url untuk foto profil
    op.add_column('users', sa.Column('avatar_url', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('users', 'avatar_url')
    op.drop_column('users', 'address')
    op.drop_column('users', 'phone')
