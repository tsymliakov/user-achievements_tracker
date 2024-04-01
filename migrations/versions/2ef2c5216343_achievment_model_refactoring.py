"""Achievment model refactoring

Revision ID: 2ef2c5216343
Revises: 63a4828c15a6
Create Date: 2024-04-01 15:41:39.390442

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ef2c5216343'
down_revision: Union[str, None] = '63a4828c15a6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('en_achievments',
    sa.Column('parent_ach_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['parent_ach_id'], ['achievments.id'], ),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('ru_achievments',
    sa.Column('parent_ach_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.ForeignKeyConstraint(['parent_ach_id'], ['achievments.id'], ),
    sa.PrimaryKeyConstraint('name')
    )
    op.drop_column('achievments', 'ru_description')
    op.drop_column('achievments', 'en_description')
    op.drop_column('achievments', 'name_ru')
    op.drop_column('achievments', 'name_en')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('achievments', sa.Column('name_en', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('achievments', sa.Column('name_ru', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('achievments', sa.Column('en_description', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('achievments', sa.Column('ru_description', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_table('ru_achievments')
    op.drop_table('en_achievments')
    # ### end Alembic commands ###
