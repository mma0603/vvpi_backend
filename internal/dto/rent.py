from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, conint

from internal.dto.vehicle import VehicleRead


class BaseRent(BaseModel):

    created_at: datetime
    deleted_at: datetime


class RentRead(BaseRent):

    class Config(object):
        orm_mode = True


class RentCreate(BaseModel):

    place_id: UUID
    vehicle_id: UUID
    hours: conint(gt=0)


class RentReadAll(RentRead):

    vehicle: VehicleRead
