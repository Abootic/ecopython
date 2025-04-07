from abc import  abstractmethod
from typing import Optional
from api.models.customer import Customer
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class ICustomerRepository(IGenericRepository[Customer]):
    
    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        pass
        
    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Customer]:
        pass
    
    @abstractmethod
    def get_by_userId(self, userid: str) -> Optional[Customer]:
        pass