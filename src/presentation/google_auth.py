from fastapi import APIRouter, HTTPException, Request
from fastapi.datastructures import URL
from fastapi.responses import RedirectResponse

from src.config import URLs, get_settings


router = APIRouter()

@router.get(URLs.GOOGLE_AUTH)
async def google_auth():
    # url : URL = URL(scope={"path": get_settings().GOOGLE_AUTHORIZATION_ENDPOINT, 
    #                        "headers": {"Host": get_settings().GOOGLE_AUTHORIZATION_ENDPOINT},
    #                        "params": {"client_id": get_settings().GOOGLE_CLIENT_ID, 
    #                                   "redirect_uri": get_settings().GOOGLE_REDIRECT_URI,
    #                                   "response_type": "code", 
    #                                   "scope": "openid email profile"}})
    url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={get_settings().GOOGLE_CLIENT_ID}&"
        f"redirect_uri={get_settings().GOOGLE_REDIRECT_URI}&"
        "response_type=code&"
        "scope=openid email profile"
    )
    return RedirectResponse(url=url)

@router.get(URLs.GOOGLE_AUTH_CALLBACK)
async def google_auth_callback(request: Request):
    print(request.query_params)

    code = request.query_params.get("code")
    if not code:
        raise HTTPException(status_code=400, detail="Missing code parameter")
