from abc import ABC, abstractmethod
from typing import List, Optional
from api.models.supplier import Supplier

class ISupplierRepository(ABC):

    @abstractmethod
    def get_by_id(self, supplier_id: int) -> Supplier:
        pass

    @abstractmethod
    def all(self) -> List[Supplier]:
        pass

    @abstractmethod
    def add(self, supplier: Supplier) -> Supplier:
        pass

    @abstractmethod
    def update(self, supplier: Supplier) -> Supplier:
        pass

    @abstractmethod
    def delete(self, supplier: Supplier) -> bool:
        pass

    @abstractmethod
    def exists_by_code(self, code: str) -> bool:
        pass

    @abstractmethod
    def count_by_market_id(self, market_id: int) -> int:
        pass

    @abstractmethod
    def get_by_code(self, code: str) -> Optional[Supplier]:
        pass

    @abstractmethod
    def get_by_userId(self, user_id: str) -> Optional[Supplier]:
        pass
