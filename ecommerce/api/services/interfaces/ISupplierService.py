from abc import ABC, abstractmethod
from typing import List
from api.dto.Supplier_dto import SupplierDTO

class ISupplierService(ABC):

  @abstractmethod
  def get_by_id(self, supplier_id: int) -> SupplierDTO:
    pass

  @abstractmethod
  def all(self) -> List[SupplierDTO]:
    pass

  @abstractmethod
  def add(self, supplier_dto: SupplierDTO) -> SupplierDTO:
    pass

  @abstractmethod
  def update(self, supplier_dto: SupplierDTO) -> SupplierDTO:
    pass

  @abstractmethod
  def delete(self, supplier_dto: SupplierDTO) -> bool:
    pass
  @abstractmethod
  def count_by_market_id(self, market_id: int) -> int:
    pass
  @abstractmethod
  def get_supplier_by_code(self, code: str) -> SupplierDTO | None:
   pass
  @abstractmethod
  def get_supplier_by_userId(self, userid: str) -> SupplierDTO | None:
   pass

