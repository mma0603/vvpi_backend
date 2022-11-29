from typing import Any, Dict
from uuid import UUID

from pydantic import BaseModel, constr, validator

from internal.usecase.utils import hashing


class BaseUser(BaseModel):

    username: constr(max_length=50)


class UserRead(BaseUser):

    id: UUID

    class Config(object):
        orm_mode = True


class UserAuth(BaseModel):

    username: constr(strip_whitespace=True, max_length=50)
    password: str

    @validator('password')
    def hashing_password(cls, v: str) -> str:  # noqa: N805
        return hashing.pbkdf2_hmac(v)


class UserCreate(BaseModel):

    username: constr(strip_whitespace=True, max_length=50)
    password: str

    @validator('password')
    def hashing_password(cls, v: str) -> str:  # noqa: N805
        return hashing.pbkdf2_hmac(v)


class UserUpdate(BaseModel):

    username: constr(strip_whitespace=True, max_length=50) | None
    password: str | None

    def dict(self, **kwargs) -> Dict[str, Any]:
        return super().dict(exclude_unset=True, **kwargs)

    @validator('password')
    def hashing_password(cls, v: str | None) -> str | None:  # noqa: N805
        if v is not None:
            return hashing.pbkdf2_hmac(v)
