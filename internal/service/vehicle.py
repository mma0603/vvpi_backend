from typing import List
from uuid import UUID

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.vehicle import VehicleCreate, VehicleUpdate
from internal.entity.vehicle import Vehicle
from internal.usecase.utils import get_session


class VehicleService(object):  # noqa: WPS214

    def __init__(
        self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.session = session
        self.repository = InjectRepository(Vehicle, session)

    async def create(self, dto: VehicleCreate) -> Vehicle:
        vehicle = self.repository.create(**dto.dict())
        return await self.repository.save(vehicle)

    async def update(self, vehicle_id: UUID, dto: VehicleUpdate) -> Vehicle:
        vehicle = self.repository.create(id=vehicle_id, **dto.dict())
        return await self.repository.save(vehicle)

    async def find(self, **attrs) -> List[Vehicle]:
        return await self.repository.find(**attrs)

    async def find_one_or_fail(self, **attrs) -> Vehicle:
        return await self.repository.find_one_or_fail(**attrs)

    async def delete(self, vehicle_id: UUID) -> None:
        await self.repository.delete(id=vehicle_id)
