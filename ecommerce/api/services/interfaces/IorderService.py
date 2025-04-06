from abc import ABC, abstractmethod
from api.dto.order_dto import OrderDTO
from typing import List

from api.wrpper.result import ResultT

class IOrderService(ABC):

    @abstractmethod
    def get_by_id(self, order_id: int) -> OrderDTO:
        pass

    @abstractmethod
    def all(self) -> List[OrderDTO]:
        pass

    @abstractmethod
    def add(self, order: OrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def update(self, order: OrderDTO) -> OrderDTO:
        pass

    @abstractmethod
    def delete(self, order: OrderDTO) -> None:
        pass

    @abstractmethod
    def calculate_supplier_profit(self, order_id: int) -> None:
        pass

    @abstractmethod
    def process_order(self, order_id: int) -> None:
        pass

    @abstractmethod
    def get_supplier_profit_for_month(self, supplier_id: int) -> float:
        pass
    @abstractmethod
    def get_orders_by_customer(self, customer_id: int) -> ResultT:
        pass
