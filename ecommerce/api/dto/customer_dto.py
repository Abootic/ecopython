from typing import Optional
from .user_dto import UserDTO  # Assuming this imports the UserDTO class

class CustomerDTO:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        code: Optional[str] = None,
        phone_number: Optional[str] = None,
        user_dto: UserDTO = None
    ):
        self.id = id
        self.user_id = user_id
        self.code = code
        self.user_dto = user_dto
        self.phone_number = phone_number

    def to_dict(self) -> dict:
        # Ensure user_dto is converted to a dictionary if it's not None
        return {
            "id": self.id,
            "code": self.code,
            "phone_number": self.phone_number,
            "user": self.user_dto.to_dict() if self.user_dto else None  # Convert user_dto to dict
        }
    
    def __str__(self) -> str:
        return f"CustomerDTO(id={self.id}, user_id={self.user_id}, code={self.code})"
