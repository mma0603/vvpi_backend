from fastapi import APIRouter

from . import payment, user, vehicle

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
router.include_router(
    vehicle.router,
    prefix='/vehicle',
    tags=['vehicle'],
)
