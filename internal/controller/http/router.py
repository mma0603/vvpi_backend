from fastapi import APIRouter, Depends

from internal.controller.http import v1
from internal.usecase.utils import dependencies

api_router = APIRouter(
    dependencies=[
        Depends(dependencies.authorization),
    ],
)
api_router.include_router(v1.router, prefix='/v1')
