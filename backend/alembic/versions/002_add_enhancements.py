"""Add class enhancements and reviews

Revision ID: 002_add_enhancements
Revises: 001_initial
Create Date: 2025-01-10

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '002_add_enhancements'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade():
    # Create ClassType enum
    class_type_enum = postgresql.ENUM(
        'YOGA', 'HIIT', 'STRENGTH', 'CARDIO', 'PILATES', 
        'CROSSFIT', 'ZUMBA', 'SPINNING', 'BOXING', 'STRETCHING',
        name='classtype'
    )
    class_type_enum.create(op.get_bind())
    
    # Create Difficulty enum
    difficulty_enum = postgresql.ENUM(
        'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'ALL_LEVELS',
        name='difficulty'
    )
    difficulty_enum.create(op.get_bind())
    
    # Add new columns to gym_classes table
    op.add_column('gym_classes', sa.Column('class_type', sa.Enum(
        'YOGA', 'HIIT', 'STRENGTH', 'CARDIO', 'PILATES', 
        'CROSSFIT', 'ZUMBA', 'SPINNING', 'BOXING', 'STRETCHING',
        name='classtype'
    ), nullable=True))
    
    op.add_column('gym_classes', sa.Column('difficulty', sa.Enum(
        'BEGINNER', 'INTERMEDIATE', 'ADVANCED', 'ALL_LEVELS',
        name='difficulty'
    ), nullable=True))
    
    op.add_column('gym_classes', sa.Column('duration', sa.Integer(), nullable=True))
    
    # Set default values for existing records
    op.execute("UPDATE gym_classes SET class_type = 'YOGA' WHERE class_type IS NULL")
    op.execute("UPDATE gym_classes SET difficulty = 'ALL_LEVELS' WHERE difficulty IS NULL")
    op.execute("UPDATE gym_classes SET duration = 60 WHERE duration IS NULL")
    
    # Make columns non-nullable after setting defaults
    op.alter_column('gym_classes', 'class_type', nullable=False)
    op.alter_column('gym_classes', 'difficulty', nullable=False)
    op.alter_column('gym_classes', 'duration', nullable=False)
    
    # Create reviews table
    op.create_table('reviews',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('class_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['class_id'], ['gym_classes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('rating >= 1.0 AND rating <= 5.0', name='valid_rating')
    )
    
    # Create indexes for better query performance
    op.create_index('idx_reviews_class_id', 'reviews', ['class_id'])
    op.create_index('idx_reviews_user_id', 'reviews', ['user_id'])
    op.create_index('idx_gym_classes_type', 'gym_classes', ['class_type'])
    op.create_index('idx_gym_classes_difficulty', 'gym_classes', ['difficulty'])
    op.create_index('idx_gym_classes_date', 'gym_classes', ['date'])


def downgrade():
    # Drop indexes
    op.drop_index('idx_gym_classes_date')
    op.drop_index('idx_gym_classes_difficulty')
    op.drop_index('idx_gym_classes_type')
    op.drop_index('idx_reviews_user_id')
    op.drop_index('idx_reviews_class_id')
    
    # Drop reviews table
    op.drop_table('reviews')
    
    # Drop new columns from gym_classes
    op.drop_column('gym_classes', 'duration')
    op.drop_column('gym_classes', 'difficulty')
    op.drop_column('gym_classes', 'class_type')
    
    # Drop enums
    difficulty_enum = postgresql.ENUM(name='difficulty')
    difficulty_enum.drop(op.get_bind())
    
    class_type_enum = postgresql.ENUM(name='classtype')
    class_type_enum.drop(op.get_bind())
