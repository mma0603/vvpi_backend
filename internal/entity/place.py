import sqlalchemy as sa
from sqlalchemy import orm

from internal.entity.base import Base
from internal.entity.rent import Rent


class Place(Base):

    __table_args__ = (
        sa.UniqueConstraint('name'),
    )

    name = sa.Column(sa.String(10), nullable=False)
    rent_cost = sa.Column(sa.Float, nullable=False)

    rent = orm.relationship(
        Rent,
        lazy='joined',
        uselist=False,
        primaryjoin=lambda: sa.and_(
            orm.remote(Rent.deleted_at) > sa.func.now(),
            orm.remote(Rent.place_id) == orm.foreign(Place.id),
        ),
    )
