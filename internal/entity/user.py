import sqlalchemy as sa

from internal.entity.base import Base
from internal.entity.mixin import TimestampMixin


class User(TimestampMixin, Base):

    __table_args__ = (
        sa.UniqueConstraint('username'),
    )

    username = sa.Column(sa.String(50), nullable=False)
    password = sa.Column(sa.String(64), nullable=False)

    balance = sa.Column(sa.Float, nullable=False, default=0)
