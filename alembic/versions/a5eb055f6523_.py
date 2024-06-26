"""empty message

Revision ID: a5eb055f6523
Revises: 030bc67846da
Create Date: 2024-04-08 15:48:17.743635

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = 'a5eb055f6523'
down_revision = '030bc67846da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('user_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.drop_index('ix_todo_todo_id', table_name='todo')
    op.create_index(op.f('ix_todo_user_id'), 'todo', ['user_id'], unique=True)
    op.drop_column('todo', 'todo_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todo', sa.Column('todo_id', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_index(op.f('ix_todo_user_id'), table_name='todo')
    op.create_index('ix_todo_todo_id', 'todo', ['todo_id'], unique=False)
    op.drop_column('todo', 'user_id')
    # ### end Alembic commands ###
