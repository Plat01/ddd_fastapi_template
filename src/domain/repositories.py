from abc import ABC, abstractmethod
from pydantic import EmailStr

from src.domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def get_by_email(self, email: EmailStr) -> User:
        ...

    @abstractmethod
    async def save(self, user: User) -> None:
        ...
