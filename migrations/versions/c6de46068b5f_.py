"""empty message

Revision ID: c6de46068b5f
Revises: 
Create Date: 2019-11-14 15:22:29.881458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6de46068b5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('major',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code_major', sa.String(length=20), nullable=True),
    sa.Column('name_major', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('province',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('studentinfo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('examinee_number', sa.String(length=30), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('registration_number', sa.String(length=30), nullable=True),
    sa.Column('international', sa.String(length=10), nullable=True),
    sa.Column('id_number', sa.String(length=20), nullable=True),
    sa.Column('birthday', sa.String(length=30), nullable=True),
    sa.Column('sex', sa.String(length=10), nullable=True),
    sa.Column('height', sa.Float(precision=10), nullable=True),
    sa.Column('high_school', sa.String(length=100), nullable=True),
    sa.Column('major', sa.String(length=100), nullable=True),
    sa.Column('major_direction', sa.String(length=100), nullable=True),
    sa.Column('view_package', sa.String(length=20), nullable=True),
    sa.Column('test_package', sa.String(length=20), nullable=True),
    sa.Column('view_score', sa.Float(precision=20), nullable=True),
    sa.Column('test_score', sa.Float(precision=20), nullable=True),
    sa.Column('final_score', sa.Float(precision=20), nullable=True),
    sa.Column('afford_fee', sa.String(length=20), nullable=True),
    sa.Column('art_science', sa.String(length=20), nullable=True),
    sa.Column('household_type', sa.String(length=50), nullable=True),
    sa.Column('phone_1', sa.String(length=30), nullable=True),
    sa.Column('phone_2', sa.String(length=30), nullable=True),
    sa.Column('province', sa.String(length=150), nullable=True),
    sa.Column('recipient', sa.String(length=100), nullable=True),
    sa.Column('note', sa.String(length=200), nullable=True),
    sa.Column('post_address', sa.String(length=200), nullable=True),
    sa.Column('input', sa.String(length=100), nullable=True),
    sa.Column('checker', sa.String(length=100), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.Column('check_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
    op.create_index(op.f('ix_studentinfo_add_time'), 'studentinfo', ['add_time'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=100), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('password', sa.String(length=32), nullable=True),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('is_admin', sa.String(length=20), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_add_time'), 'user', ['add_time'], unique=False)
    op.create_table('log',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ip', sa.String(length=100), nullable=True),
    sa.Column('reason', sa.String(length=600), nullable=True),
    sa.Column('add_time', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_log_add_time'), 'log', ['add_time'], unique=False)
    op.create_table('majordirection',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name_direction', sa.String(length=100), nullable=True),
    sa.Column('major_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['major_id'], ['major.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('majordirection')
    op.drop_index(op.f('ix_log_add_time'), table_name='log')
    op.drop_table('log')
    op.drop_index(op.f('ix_user_add_time'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_studentinfo_add_time'), table_name='studentinfo')
    op.drop_table('studentinfo')
    op.drop_table('province')
    op.drop_table('major')
    # ### end Alembic commands ###
