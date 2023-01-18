from app.core.config import settings
from fastapi import APIRouter

from app.api.api_v1.endpoints import items, login, users, utils

api_v1 = APIRouter(prefix=settings.API_V1_STR)
api_v1.include_router(login.router, tags=["login"])
api_v1.include_router(users.router, prefix="/users", tags=["users"])
api_v1.include_router(utils.router, prefix="/utils", tags=["utils"])
api_v1.include_router(items.router, prefix="/items", tags=["items"])
