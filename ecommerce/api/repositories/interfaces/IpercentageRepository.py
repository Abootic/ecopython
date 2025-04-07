from abc import  abstractmethod
from typing import Optional
from api.models.percentage import Percentage
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class IPercentageRepository(IGenericRepository[Percentage]):
    
    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        pass
        
    @abstractmethod
    def get_by_supplier(self, supplier_id: int) -> Optional[Percentage]:
        pass
    
    @abstractmethod
    def assign_percentage_value_to_suppliers(self, market_id: int) -> int:
        pass