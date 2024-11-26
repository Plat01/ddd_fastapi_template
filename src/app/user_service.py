from abc import ABC, abstractmethod
from typing import Any
from fastapi import Request

from src.config import get_settings
from src.domain.entities import User
from src.domain.repositories import UserRepository


class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, userinfo: dict[str, Any]) -> User:
        # TOOD: implement for all kind of users
        email = userinfo["email"]
        user = await self.user_repository.get_by_email(email)
        if user:
            user.name = userinfo["name"]
            user.picture = userinfo.get("picture")
            await self.user_repository.save(user)
        else:
            user = User(
                email=userinfo["email"],
                name=userinfo["name"],
                picture=userinfo.get("picture"),
            )
            await self.user_repository.save(user)
        return user   
    

# class UserServiceFactory:
#     def __init__(self, user_repository: UserRepository):
#         self.user_repository = user_repository
#         self.user_service = UserService(self.user_repository)
    
#     def get_user_service(self) -> UserService:
#         return self.user_service

class AuthService(ABC):

    @abstractmethod
    async def get_authorization_url(self) -> str:
        pass


if __name__ == "__main__":
    pass
