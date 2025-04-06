from typing import Optional
from .user_dto import UserDTO
from datetime import datetime

class SupplierDTO:
    def __init__(
        self,
        id: Optional[int] = None,
        user_id: Optional[int] = None,
        market_id: Optional[int] = None,
        code: Optional[str] = None,
        user_dto: UserDTO = None,
        join_date: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.market_id = market_id
        self.code = code
        self.user_dto = user_dto
        self.join_date = join_date

    def to_dict(self) -> dict:
        return {
            "id": self.id,  # Ensure this is an integer
            "user_id": self.user_id,  # Ensure this is an integer
            "market_id": self.market_id,  # Ensure this is an integer
            "code": self.code,
            "user_dto": self.user_dto.to_dict() if self.user_dto else None,  # Serialize user_dto if present
            "join_date": self.join_date.isoformat() if self.join_date else None
        }

    def __str__(self) -> str:
        return f"SupplierDTO(id={self.id}, user_id={self.user_id}, market_id={self.market_id}, code={self.code})"
    
    @staticmethod
    def from_model(supplier):
        """
        Convert a Supplier model instance to a SupplierDTO.
        """
        # Assuming `supplier` is a Django model instance
        user_dto = UserDTO.from_model(supplier.user)  # Assuming a from_model method in UserDTO
        return SupplierDTO(
            id=supplier.id,
            user_id=supplier.user_id,
            market_id=supplier.market_id,
            code=supplier.code,
            user_dto=user_dto,
            join_date=supplier.join_date
        )

