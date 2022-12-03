from datetime import timedelta
from typing import List
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.place import PlaceFilter
from internal.dto.rent import RentCreate
from internal.entity.place import Place
from internal.entity.rent import Rent
from internal.entity.vehicle import Vehicle
from internal.service.vehicle import VehicleService
from internal.usecase.utils import get_session


class PlaceService(object):  # noqa: WPS214

    def __init__(
        self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.session = session
        self.repository = InjectRepository(Place, session)
        self.rent_repository = InjectRepository(Rent, session)
        self.vehicle_service = VehicleService(session)

    async def find(self, dto: PlaceFilter, **attrs) -> List[Place]:
        where = {Place.name.ilike('%{0}%'.format(dto.name))}
        if dto.available is False:
            where.add(Place.rent.has(Rent.deleted_at > sa.func.now()))

        places = await self.repository.find(*where, **attrs)
        if dto.available:
            places = list(filter(lambda p: p.rent is None, places))

        return places

    async def find_user(self, user_id: UUID) -> List[Place]:
        return await self.repository.find(
            Place.rent.has(sa.and_(
                Rent.deleted_at > sa.func.now(),
                Rent.vehicle.has(Vehicle.user_id == user_id),
            )),
        )

    async def rent(self, dto: RentCreate) -> Rent:
        rent = self.rent_repository.create(
            **dto.dict(exclude={'hours'}),
            deleted_at=sa.func.now() + timedelta(hours=dto.hours),
        )
        return await self.rent_repository.save(rent)
