"""empty message

Revision ID: 916f3b4e6114
Revises: 
Create Date: 2024-04-05 12:22:16.971384

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel

# revision identifiers, used by Alembic.
revision = '916f3b4e6114'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('authsession',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('session_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('expiration', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_authsession_session_id'), 'authsession', ['session_id'], unique=True)
    op.create_index(op.f('ix_authsession_user_id'), 'authsession', ['user_id'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('password_hash', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email_id'), 'user', ['email_id'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_authsession_user_id'), table_name='authsession')
    op.drop_index(op.f('ix_authsession_session_id'), table_name='authsession')
    op.drop_table('authsession')
    # ### end Alembic commands ###
