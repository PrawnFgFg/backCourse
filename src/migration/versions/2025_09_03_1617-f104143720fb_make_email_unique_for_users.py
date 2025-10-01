"""make email unique for users

Revision ID: f104143720fb
Revises: 9e227c1390b2
Create Date: 2025-09-03 16:17:36.937301

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision: str = "f104143720fb"
down_revision: Union[str, Sequence[str], None] = "9e227c1390b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
