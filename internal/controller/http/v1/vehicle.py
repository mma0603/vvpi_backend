from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, status

from internal.dto.user.request import RequestUser
from internal.dto.vehicle import (
    VehicleBody,
    VehicleCreate,
    VehicleRead,
    VehicleUpdate,
)
from internal.entity.vehicle import Vehicle
from internal.service.vehicle import VehicleService
from internal.usecase.utils import (
    SuccessfulResponse,
    dependencies,
    response,
)

router = APIRouter()


@router.get(
    path='',
    response_model=List[VehicleRead],
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    )
)
async def read_vehicles(
    vehicle_service: VehicleService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> List[Vehicle]:
    return await vehicle_service.find(user_id=request_user.id)


@router.post(
    path='',
    response_model=VehicleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_vehicle(
    dto: VehicleBody,
    vehicle_service: VehicleService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> Vehicle:
    return await vehicle_service.create(
        VehicleCreate(user_id=request_user.id, **dto.dict()),
    )


@router.patch(
    path='/{vehicle_id}',
    response_model=VehicleRead,
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ),
)
async def update_vehicle(
    vehicle_id: UUID,
    dto: VehicleUpdate,
    vehicle_service: VehicleService = Depends(),
    _: RequestUser = Depends(dependencies.get_request_user),
) -> Vehicle:
    return await vehicle_service.update(vehicle_id, dto)


@router.delete(
    path='/{vehicle_id}',
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ),
)
async def update_vehicle(
    vehicle_id: UUID,
    vehicle_service: VehicleService = Depends(),
    _: RequestUser = Depends(dependencies.get_request_user),
) -> SuccessfulResponse:
    await vehicle_service.delete(vehicle_id)
    return SuccessfulResponse()
