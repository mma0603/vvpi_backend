from uuid import UUID

from pydantic import BaseModel

from internal.dto.session import Session


class RequestUser(BaseModel):

    id: UUID
    session: Session
