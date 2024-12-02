from fastapi import APIRouter, HTTPException, Request
from authlib.integrations.starlette_client import OAuthError
from fastapi.responses import JSONResponse

from src.config import URLs
from src.infrastructure.auth import oauth


router = APIRouter()

@router.get(URLs.YANDEX_AUTH, name="yandex_auth")
async def yandex_auth(request: Request):
    try:
        access_token = await oauth.yandex.authorize_access_token(request)
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    user_data = await oauth.yandex.parse_id_token(request, access_token)
    return JSONResponse(content=user_data)

@router.get(URLs.YANDEX_AUTH_CALLBACK)
async def yandex_auth_callback(request: Request):
    """
        {
    "id": "1991469931",
    "login": "nphne-oktu27ae",
    "client_id": "08ecaa08e43e496193a829f42c68675f",
    "display_name": "+79199173395",
    "real_name": "",
    "first_name": "",
    "last_name": "",
    "sex": null,
    "default_email": "",
    "emails": [],
    "psuid": "1.AAzaig.vP6mS84IhogbAAhMw7ERcA.E7ytcB1vJQevAYp7RRyaYQ"
    }

    Args:
        request (Request): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        access_token = await oauth.yandex.authorize_access_token(request)
        print(access_token)
        # test-main     | {'access_token': 'y0_AgAAAAB2s2trAAzaigAAAAEaseSLAACYGOTIAFBF5IsxUvkKx7tRAVoWJg', 'expires_in': 31535650, 'refresh_token': '1:bOCemcaMXFERA7bT:gh7lVYqbq7CJuFg-XL4mmMAtI7VBjKSe1jP5dqx40fyfGnxtqsZZgIJQ8tt71eyricFc7zEns0GSjs_LqQ:xPU0XAlDJtRdI-q95OUSpw', 'scope': 'login:email login:info', 'token_type': 'bearer', 'expires_at': 1764626510}
    except OAuthError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Fetch user data using the access token
    try:
        resp = await oauth.yandex.get('https://login.yandex.ru/info', token=access_token)
        user_data = resp.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch user info: {str(e)}")
    
    return JSONResponse(content=user_data)

@router.get(URLs.YANDEX_LOGIN)
async def yandex_logout(request: Request):
    redirect_url = request.url_for('yandex_auth_callback')
    print(redirect_url)
    return await oauth.yandex.authorize_redirect(request, redirect_url)
