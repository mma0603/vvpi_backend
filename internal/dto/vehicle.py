from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, constr


class BaseVehicle(BaseModel):

    model: str
    license_plate: str


class VehicleRead(BaseVehicle):

    id: UUID

    class Config(object):
        orm_mode = True


class VehicleBody(BaseModel):

    model: constr(max_length=100)
    license_plate: constr(max_length=10)


class VehicleCreate(VehicleBody):

    user_id: UUID


class VehicleUpdate(BaseModel):

    model: constr(max_length=100) | None
    license_plate: constr(max_length=10) | None

    def dict(self, **kwargs) -> Dict[str, Any]:
        return super().dict(exclude_unset=True, **kwargs)
