from fastapi import APIRouter, Depends

from internal.dto.payment import PaymentBody
from internal.dto.user.request import RequestUser
from internal.service.user import UserService
from internal.usecase.utils import dependencies
from internal.usecase.utils import SuccessfulResponse

router = APIRouter()


@router.post(path='')
async def accrual(
    dto: PaymentBody,
    user_service: UserService = Depends(),
    request_user: RequestUser = Depends(dependencies.get_request_user),
) -> SuccessfulResponse:
    await user_service.accrual(request_user.id, dto.amount)
    return SuccessfulResponse()
