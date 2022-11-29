from datetime import datetime

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from redis.asyncio import Redis

from internal.config import settings
from internal.dto.user.request import RequestUser
from internal.usecase.utils import get_redis

http_bearer = HTTPBearer(auto_error=False)


async def authorization(
    request: Request,
    redis: Redis = Depends(get_redis),
    credentials: HTTPAuthorizationCredentials | None = Depends(http_bearer),
) -> None:
    request.scope['user'] = None

    if credentials is None:
        return

    session = settings.REDIS_SESSION.format(credentials.credentials)
    request_user_row = await redis.get(session)
    if request_user_row is None:
        return

    request_user = RequestUser.parse_raw(request_user_row)
    if request_user.session.expires < datetime.utcnow():
        await redis.delete(session)
        return

    request.scope['user'] = request_user


async def get_request_user(request: Request) -> RequestUser:
    if request.user is None:
        raise HTTPException(
            detail='Invalid authentication credentials',
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return request.user
