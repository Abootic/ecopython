from django.apps import apps
from api.dto.user_dto import UserDTO

class UserMapper:
    @staticmethod
    def to_dto(user) -> UserDTO:
        return UserDTO(
            id=user.id,
            username=user.username,
            user_type=user.user_type,
            email=user.email,
            password=None  # Don't include the password
        )

    @staticmethod
    def to_model(user) -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "email": user.email,
            "password": None  # Don't include the password
        }