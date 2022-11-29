import secrets

from fastapi import APIRouter, Depends, HTTPException, Request, status
from redis.asyncio import Redis

from internal.config import settings
from internal.dto.session import Session
from internal.dto.user import (
    UserAuth,
    UserCreate,
    UserRead,
    UserUpdate,
)
from internal.dto.user.request import RequestUser
from internal.entity.user import User
from internal.service.user import UserService
from internal.usecase.utils import (
    SuccessfulResponse,
    dependencies,
    get_redis,
    response,
)

router = APIRouter()


@router.get(
    path='',
    response_model=UserRead,
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ) | response.HTTP_404_NOT_FOUND(
        'User not found',
    ),
)
async def read_user(
    user_service: UserService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> User:
    return await user_service.find_one_or_fail(id=request_user.id)


@router.post(
    path='',
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    dto: UserCreate,
    user_service: UserService = Depends(),
) -> User:
    return await user_service.create(dto)


@router.patch(
    path='',
    response_model=UserRead,
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ),
)
async def update_user(
    dto: UserUpdate,
    user_service: UserService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> User:
    return await user_service.update(request_user.id, dto)


@router.post(
    path='/login',
    response_model=RequestUser,
    responses=response.HTTP_401_UNAUTHORIZED(
        'Incorrect password',
    ) | response.HTTP_403_FORBIDDEN(
        'Authorized',
    ) | response.HTTP_404_NOT_FOUND(
        'User not found',
    ),
)
async def login(
    dto: UserAuth,
    request: Request,
    redis: Redis = Depends(get_redis),
    user_service: UserService = Depends(),
) -> RequestUser:
    if request.user is not None:
        raise HTTPException(
            detail='Authorized',
            status_code=status.HTTP_403_FORBIDDEN,
        )

    user = await user_service.find_one_or_fail(
        username=dto.username,
    )
    if not secrets.compare_digest(dto.password, user.password):
        raise HTTPException(
            detail='Incorrect password',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    session = Session()
    request_user = RequestUser(
        id=user.id,
        session=session,
    )
    await redis.set(
        name=settings.REDIS_SESSION.format(session.id),
        value=request_user.json(),
        exat=request_user.session.expires,
    )
    return request_user


@router.delete(
    path='/logout',
    responses=response.HTTP_401_UNAUTHORIZED(
        'Invalid authentication credentials',
    ) | SuccessfulResponse.schema(),
)
async def logout(
    redis: Redis = Depends(get_redis),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> SuccessfulResponse:
    await redis.delete(settings.REDIS_SESSION.format(request_user.session.id))
    return SuccessfulResponse()
