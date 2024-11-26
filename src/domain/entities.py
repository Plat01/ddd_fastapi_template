from uuid import UUID, uuid4
from beanie import PydanticObjectId
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    """
        User Model
    """
    id: str | PydanticObjectId  # ? is it good to bind domani area to  MongoDB-specific types ?
    email: EmailStr  # poetry add email-validator
    verified_email: bool
    name: str
    picture: str | None
    locale: str
    phone_number: str | None


class GoogleUser(User):
    """
        Google User Model
    """
    pass 

class VKUser(User):
    """
        VK User Model
    """
    pass

class YandexUser(User):
    """
        Yandex User Model
    """
    pass
