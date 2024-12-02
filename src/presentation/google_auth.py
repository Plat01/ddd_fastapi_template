from fastapi import APIRouter, HTTPException, Request
from fastapi.datastructures import URL
from fastapi.responses import JSONResponse, RedirectResponse

from src.config import URLs, get_settings
from src.infrastructure.auth import oauth


router = APIRouter()

# TODO: find outh if I need it
@router.get(URLs.GOOGLE_AUTH)
async def google_auth(request: Request):
    try:
        token = await oauth.google.authorize_access_token(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    user_info = token.get('userinfo')
    if user_info:
        request.session['user'] = dict(user_info)
        return RedirectResponse(url='/')
    raise HTTPException(status_code=400, detail="Could not fetch user info")

@router.get(URLs.GOOGLE_AUTH_CALLBACK, name="google_auth_callback")
async def google_auth_callback(request: Request):
    """
    Function gets responce like http://localhost:8000/api/v1/auth/google/callback?state=RK75rQqSUSl65l1rCaNeLCa3PsnhmN&code=4%2F0AeanS0bMin2Xu-jskj7UVz6rqsTeACRJ8S_Ua7uiB8FzsxI-mFZBlsX6WJOeZD9-KfkEFw&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email&authuser=0&prompt=consent
    which can containn sencetive data and shudn't been seen by users frontend in production
    Args:
        param (str): _description_
        request (Request): _description_

    Raises:
        HTTPException: _description_
    """
    try:
        # Exchange the authorization code for an access token
        token = await oauth.google.authorize_access_token(request)
        print(token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to authorize: {str(e)}")

    # try:
    #     # Use the token to get the user's profile info
    #     user_info_response = await oauth.google.parse_id_token(request, token)
    # except Exception as e:
    #     raise HTTPException(status_code=400, detail=f"Failed to fetch user info: {str(e)}")
    # return JSONResponse(content=user_info_response)
    user_info = token.get("userinfo")
    if not user_info:
        # If userinfo is not present, use the access token to fetch user info from Google
        try:
            resp = await oauth.google.get('https://www.googleapis.com/oauth2/v3/userinfo', token=token)
            user_info = resp.json()
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to fetch user info: {str(e)}")


    # `user_info_response` contains all the user information returned by Google
    return JSONResponse(content=user_info)
    
# @router.post(URLs.GOOGLE_AUTH_CALLBACK)
# async def google_auth_callback(request: Request): 
#     """
#     POst request to http://localhost:8000/api/v1/auth/google/callback
    
#     Args:
#         request (Request): _description_

#     Raises:
#         HTTPException: _description_
#     """
#     print(request.query_params)

#     code = request.query_params.get("code")
#     if not code:
#         raise HTTPException(status_code=400, detail="Missing code parameter")
    
@router.get(URLs.GOOGLE_LOGIN)
async def google_login(request: Request):
    redirect_uri = request.url_for(google_auth_callback.__name__)
    try:
        responce = await oauth.google.authorize_redirect(request, redirect_uri)
        return responce
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
