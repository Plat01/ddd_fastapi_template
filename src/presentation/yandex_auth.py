from fastapi import APIRouter

from src.config import URLs


router = APIRouter()

@router.get(URLs.YANDEX_AUTH)
async def yandex_auth():
    return {"message": "Yandex Auth"}
