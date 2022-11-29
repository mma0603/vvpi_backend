from uuid import UUID

from fastapi import Depends
from pytorm.repository import InjectRepository
from sqlalchemy.ext.asyncio import AsyncSession

from internal.dto.user import UserCreate, UserUpdate
from internal.entity.user import User
from internal.usecase.utils import get_session


class UserService(object):  # noqa: WPS214

    def __init__(
        self, session: AsyncSession = Depends(get_session),
    ) -> None:
        self.session = session
        self.repository = InjectRepository(User, session)

    async def create(self, dto: UserCreate) -> User:
        user = self.repository.create(**dto.dict())
        return await self.repository.save(user)

    async def update(self, user_id: UUID, dto: UserUpdate) -> User:
        user = self.repository.create(id=user_id, **dto.dict())
        return await self.repository.save(user)

    async def find_one_or_fail(self, **attrs) -> User:
        return await self.repository.find_one_or_fail(**attrs)
