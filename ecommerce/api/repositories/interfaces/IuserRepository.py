from abc import ABC, abstractmethod
from typing import List
from api.models.user import User

class IUserRepository(ABC):
  
  @abstractmethod
  def get_by_id(self, user_id: int) -> User:
    pass
  @abstractmethod
  def all(self) -> List[User]:
    pass
  @abstractmethod
  def create(self, user: User) ->User:
    pass

  @abstractmethod
  def update(self, user_dto: User) ->User:
    pass

  @abstractmethod
  def delete(self, user_dto: User) ->User:
    pass
  @abstractmethod
  def update_user_role(self, user_id: int, new_role: str) -> User:
    pass
