from dataclasses import dataclass
from uuid import UUID

from fastapi import Query
from pydantic import BaseModel

from internal.dto.rent import RentReadAll


class BasePlace(BaseModel):

    name: str
    rent_cost: float

    rent: RentReadAll | None


class PlaceRead(BasePlace):

    id: UUID

    class Config(object):
        orm_mode = True


@dataclass
class PlaceFilter(object):

    name: str = Query('')
    available: bool | None = Query(None)
