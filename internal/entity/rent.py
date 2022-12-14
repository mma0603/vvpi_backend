import sqlalchemy as sa
from sqlalchemy import orm
from sqlalchemy.dialects import postgresql as psql

from internal.entity.base import Base
from internal.entity.mixin import TimestampMixin
from internal.entity.vehicle import Vehicle


class Rent(TimestampMixin, Base):

    place_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey('place.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    vehicle_id = sa.Column(
        psql.UUID(as_uuid=True),
        sa.ForeignKey('vehicle.id', ondelete='CASCADE'),
        index=True,
        nullable=False,
    )
    deleted_at = sa.Column(
        sa.DateTime,
        nullable=False,
        server_default=sa.FetchedValue(),
    )

    vehicle = orm.relationship(Vehicle, lazy='joined')
