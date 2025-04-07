from abc import abstractmethod
from datetime import datetime
from typing import List, Dict
from api.models.supplierProfit import SupplierProfit
from api.repositories.interfaces.IGenericRepository import IGenericRepository

class ISupplierProfitRepository(IGenericRepository[SupplierProfit]):
    
    @abstractmethod
    def get_total_profit_for_market(self, market_id: int, month: datetime) -> float:
        pass

    @abstractmethod
    def get_supplier_percentages(self, market_id: int) -> List[Dict]:
        pass

    @abstractmethod
    def update_or_create_supplier_profit(self, supplier, month: datetime, profit: float) -> SupplierProfit:
        pass