from abc import ABC, abstractmethod
from typing import List
from django.utils import timezone # type: ignore
from api.models.supplierProfit import SupplierProfit

class ISupplierProfitRepository(ABC):
    
    @abstractmethod
    def get_total_profit_for_market(self, market_id: int, month: timezone) -> float:
        """
        Get the total profit for the market in the given month.
        """
        pass

    @abstractmethod
    def get_supplier_percentages(self, market_id: int) -> List[dict]:
        """
        Get the percentages for suppliers in a given market.
        """
        pass

    @abstractmethod
    def all(self) -> List[SupplierProfit]:
        """
        Get all supplier profit records.
        """
        pass

    @abstractmethod
    def update_or_create_supplier_profit(self, supplier, month: timezone, profit: float) -> SupplierProfit:
        """
        Update or create a supplier profit record.
        """
        pass
