from abc import ABC, abstractmethod
from typing import List
from api.dto.product_dto import ProductDTO

class IProductService(ABC):

  @abstractmethod
  def get_by_id(self, product_id: int) -> ProductDTO:
    pass

  @abstractmethod
  def all(self) -> List[ProductDTO]:
    pass

  @abstractmethod
  def add(self, product_dto: ProductDTO) -> ProductDTO:
    pass

  @abstractmethod
  def update(self, product_dto: ProductDTO) -> ProductDTO:
    pass

  @abstractmethod
  def delete(self, product_dto: ProductDTO) -> bool:
    pass
