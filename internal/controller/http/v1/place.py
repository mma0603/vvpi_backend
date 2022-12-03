from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from internal.dto.place import PlaceFilter, PlaceRead
from internal.dto.rent import RentCreate
from internal.dto.user.request import RequestUser
from internal.entity.place import Place
from internal.service.place import PlaceService
from internal.usecase.utils import (
    SuccessfulResponse,
    dependencies,
    response,
)

router = APIRouter()


@router.get(
    path='',
    response_model=List[PlaceRead],
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ),
)
async def read_places(
    dto: PlaceFilter = Depends(),
    place_service: PlaceService = Depends(),
    _: RequestUser = Depends(dependencies.get_request_user),
) -> List[Place]:
    return await place_service.find(dto)


@router.get(
    path='/my',
    response_model=List[PlaceRead],
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ),
)
async def read_my_places(
    place_service: PlaceService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> List[Place]:
    return await place_service.find_user(request_user.id)


@router.post(
    path='',
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ) | response.HTTP_403_FORBIDDEN(
        'Not your vehicle',
    ) | response.HTTP_404_NOT_FOUND(
        'Already rent',
    ) | response.HTTP_403_FORBIDDEN(
        'Not enough money',
    ),
    status_code=status.HTTP_201_CREATED,
)
async def rent_place(
    dto: RentCreate,
    place_service: PlaceService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> SuccessfulResponse:
    vehicle = await place_service.vehicle_service.find_one_or_fail(
        id=dto.vehicle_id,
    )
    if vehicle.user_id != request_user.id:
        raise HTTPException(
            detail='Not your vehicle',
            status_code=status.HTTP_403_FORBIDDEN,
        )
    place = await place_service.find_one_or_fail(id=dto.place_id)
    if place.rent is not None:
        raise HTTPException(
            detail='Already rent',
            status_code=status.HTTP_404_NOT_FOUND,
        )

    user = await place_service.user_service.find_one_or_fail(id=request_user.id)
    if place.rent_cost * dto.hours > user.balance:
        raise HTTPException(
            detail='Not enough money',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    await place_service.rent(dto)
    await place_service.user_service.withdrawal(
        user.id, place.rent_cost * dto.hours,
    )
    return SuccessfulResponse()
