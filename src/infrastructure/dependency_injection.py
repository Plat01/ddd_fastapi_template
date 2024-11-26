from src.app.user_service import UserService
from src.infrastructure.repositories import BeanieUserRepository


def get_user_service() -> UserService:
    user_repository = BeanieUserRepository()
    return UserService(user_repository)
