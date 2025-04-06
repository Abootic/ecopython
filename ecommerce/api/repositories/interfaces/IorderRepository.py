from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional
from api.models.order import Order
from api.models.product import Product
from api.models.supplier import Supplier
from api.models.supplierProfit import SupplierProfit


class IOrderRepository(ABC):

    @abstractmethod
    def get_by_id(self, order_id: int) -> Order:
        pass

    @abstractmethod
    def all(self) -> List[Order]:
        pass

    @abstractmethod
    def add(self, order: Order) -> Order:
        pass

    @abstractmethod
    def update(self, order: Order) -> Order:
        pass

    @abstractmethod
    def delete(self, order: Order) -> Order:
        pass
    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> List[Order]:
        pass

    @abstractmethod
    def get_supplier_by_product(self, product: Product) -> Supplier:
        pass

    @abstractmethod
    def get_or_create_supplier_profit(self, supplier: Supplier, month: date) -> SupplierProfit:
        pass

    @abstractmethod
    def update_supplier_profit(self, supplier_profit: SupplierProfit, profit_value: float) -> SupplierProfit:
        pass

    @abstractmethod
    def get_orders_by_supplier(self, supplier: Supplier) -> List[Order]:
        pass
    @abstractmethod
    def get_supplier_profit_for_month(self, supplier_id: int) -> Optional[SupplierProfit]:
        pass
    @abstractmethod
    def update_or_create_supplier_profit(self,supplier, order_profit):
        pass