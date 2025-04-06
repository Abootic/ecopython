from abc import ABC, abstractmethod
from typing import List

from api.dto.Supplier_dto import SupplierDTO

class ISupplierProfitService(ABC):
    @abstractmethod
    def update_or_create_profit(self, market_id, month):
        pass
    @abstractmethod
    def all(self) -> List[SupplierDTO]:
        pass