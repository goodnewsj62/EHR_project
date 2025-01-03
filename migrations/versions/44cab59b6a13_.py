"""empty message

Revision ID: 44cab59b6a13
Revises: 
Create Date: 2025-01-03 12:58:31.183634

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "44cab59b6a13"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("password", sa.Text(), nullable=False),
        sa.Column("email_verified", sa.Boolean(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_table(
        "patient",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("fullname", sa.String(100), nullable=False),
        sa.Column("email", sa.String(100), nullable=False),
        sa.Column("phone", sa.String(16), nullable=False),
        sa.Column("address", sa.Text(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column(
            "gender",
            sa.Enum("MALE", "FEMALE", "BISEXUAL", "OTHERS", name="gender"),
            nullable=False,
        ),
        sa.Column("ethnicity", sa.String(10), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "patient_record",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("is_immunized", sa.Boolean(), nullable=False),
        sa.Column("appointment", sa.DateTime(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["patient_id"],
            ["patient.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "image",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("blob", sa.Text(), nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=False),
        sa.Column("record_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["record_id"],
            ["patient_record.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("image")
    op.drop_table("patient_record")
    op.drop_table("patient")
    op.drop_table("users")
    # ### end Alembic commands ###
