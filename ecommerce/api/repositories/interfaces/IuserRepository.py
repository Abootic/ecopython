from abc import  abstractmethod

from api.models.user import User
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class IUserRepository(IGenericRepository[User]):
    
    @abstractmethod
    def update_user_role(self, user_id: int, new_role: str) -> User:
        pass
        
    @abstractmethod
    def add(self, user: User, password: str) -> User:
        pass