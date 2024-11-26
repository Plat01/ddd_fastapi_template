from fastapi import APIRouter

from src.config import URLs
from src.presentation import google_auth, yandex_auth


api_router = APIRouter()

api_router.include_router(google_auth.router, prefix=URLs.AUTH, tags=["Google"])
api_router.include_router(yandex_auth.router, prefix=URLs.AUTH, tags=["Yandex"])
