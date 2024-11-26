from typing import Any
from fastapi import Request
from google_auth_oauthlib.flow import Flow # poetry add google-auth-oauthlib

from src.app.user_service import UserService
from src.config import get_settings
from src.domain.entities import User  

class GoogleAuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service
        self.client_secrets = {
            "web": {
                "client_id": get_settings().GOOGLE_CLIENT_ID,
                "project_id": "my-project-id",
                # "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "auth_uri": get_settings().GOOGLE_AUTHORIZATION_ENDPOINT,
                # "token_uri": "https://oauth2.googleapis.com/token",
                "token_uri": get_settings().GOOGLE_TOKEN_ENDPOINT,
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_secret": get_settings().GOOGLE_CLIENT_SECRET,
                "redirect_uris": [get_settings().GOOGLE_REDIRECT_URI],
            }
        }


    def get_authorization_url(self, state: str) -> str:
        flow = Flow.from_client_config(
            client_config=self.client_secrets,
            scopes=["openid", "email", "profile"],
            redirect_uri=self.client_secrets["web"]["redirect_uris"][0],
        )
        flow.params["access_type"] = "offline"
        flow.params["include_granted_scopes"] = "true"
        flow.params["state"] = state
        authorization_url, _ = flow.authorization_url(prompt="consent")
        return authorization_url

    async def authorize_user(self, request: Request) -> User:
        state = request.session.get("state")
        flow = Flow.from_client_config(
            client_config=self.client_secrets,
            scopes=["openid", "email", "profile"],
            redirect_uri=self.client_secrets["web"]["redirect_uris"][0],
            state=state,
        )
        flow.fetch_token(authorization_response=str(request.url))

        credentials = flow.credentials
        token = credentials.token

        # Use the credentials to get user info
        userinfo = await self.get_user_info(token)
        user = await self.user_service.authenticate_user(userinfo)
        return user

    async def get_user_info(self, token: str) -> dict[str, Any]:
        from googleapiclient.discovery import build  # poetry add google-api-python-client
        from google.oauth2.credentials import Credentials

        credentials = Credentials(token)
        service = build('oauth2', 'v2', credentials=credentials)
        userinfo = service.userinfo().get().execute()
        return userinfo
