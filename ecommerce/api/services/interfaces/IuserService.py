from abc import ABC, abstractmethod
from typing import List
from api.dto.user_dto import UserDTO

class IUserService(ABC):

  @abstractmethod
  def get_user_by_id(self, user_id: int) -> UserDTO:
    pass
  @abstractmethod
  def all(self) -> List[UserDTO]:
    pass

  @abstractmethod
  def create_user(self, user_dto: UserDTO) -> UserDTO:
    pass

  @abstractmethod
  def update_user(self, user_dto: UserDTO) -> UserDTO:
    pass

  @abstractmethod
  def delete_user(self, user_id: int) -> bool:
    pass
  @abstractmethod
  def update_user_role(self, user_id: int, new_role: str) -> UserDTO:
    pass