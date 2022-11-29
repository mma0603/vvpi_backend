import sqlalchemy as sa
from sqlalchemy.dialects import postgresql as psql

from internal.entity.base import Base


class Vehicle(Base):

    __table_args__ = (
        sa.UniqueConstraint('license_plate'),
    )

    model = sa.Column(sa.String(100), nullable=False)
    license_plate = sa.Column(sa.String(10), nullable=False)

    user_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey('user.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
