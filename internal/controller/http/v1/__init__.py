from fastapi import APIRouter

from . import payment, user

router = APIRouter()
router.include_router(
    user.router,
    prefix='/user',
    tags=['user'],
)
router.include_router(
    payment.router,
    prefix='/payment',
    tags=['payment'],
)
