from fastapi import APIRouter

from src.config import URLs


router = APIRouter()

@router.get(URLs.GOOGLE_AUTH)
async def google_auth():
    return {"message": "Google Auth"}
