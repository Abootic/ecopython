from abc import ABC, abstractmethod
from typing import List
from api.dto.customer_dto import CustomerDTO
from api.wrpper.result import ResultT

class ICustomerService(ABC):

  @abstractmethod
  def get_by_id(self, customer_id: int) -> CustomerDTO:
    pass

  @abstractmethod
  def all(self) -> List[CustomerDTO]:
    pass

  @abstractmethod
  def add(self, customer_dto: CustomerDTO) -> CustomerDTO:
    pass

  @abstractmethod
  def update(self, supplier_dto: CustomerDTO) -> CustomerDTO:
    pass

  @abstractmethod
  def delete(self, supplier_dto: CustomerDTO) -> bool:
    pass
  @abstractmethod
  def get_supplier_by_code(self, code: str) -> CustomerDTO | None:
   pass
  @abstractmethod
  def get_customer_by_userId(self, userid: str) -> ResultT:
   pass

