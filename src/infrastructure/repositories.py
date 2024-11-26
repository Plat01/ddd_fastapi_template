from beanie import Document
from pydantic import EmailStr

from src.domain.entities import User
from src.domain.repositories import UserRepository


class UserDocument(Document):
    email: str
    name: str
    picture: str | None
    locale: str
    verified_email: bool

    class Settings:
        name = "users"

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=self.email,
            name=self.name,
            picture=self.picture,
            locale=self.locale,
            verified_email=self.verified_email,
        )
    
    @classmethod
    def from_entity(cls, user: User) -> "UserDocument":
        return cls(
            id=user.id,
            email=user.email,
            name=user.name,
            picture=user.picture,
            locale=user.locale,
            verified_email=user.verified_email,
        )
    

class BeanieUserRepository(UserRepository):
    async def get_by_email(self, email: EmailStr) -> User | None:
        user_doc = await UserDocument.find_one(UserDocument.email == email)
        if user_doc:
            return user_doc.to_entity()
        return None

    async def save(self, user: User) -> None:
        user_doc = UserDocument.from_entity(user)
        await user_doc.save()