import secrets
from datetime import datetime, timedelta

from pydantic import BaseModel, Field

from internal.config import settings


class Session(BaseModel):

    id: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    expires: datetime = Field(
        default_factory=lambda:
            datetime.utcnow() + timedelta(**settings.SESSION_TIMEDELTA),
    )
