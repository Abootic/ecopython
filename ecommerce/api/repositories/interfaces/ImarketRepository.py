from abc import ABC, abstractmethod
from typing import List
from api.models.market import Market

class IMarketRepository(ABC):
  """
  Interface for repository pattern to manage market entities.
  """
  
  @abstractmethod
  def get_by_id(self, market_id: int) -> Market:

    pass

  @abstractmethod
  def all(self) -> List[Market]:

    pass

  @abstractmethod
  def add(self, market: Market) -> Market:

    pass

  @abstractmethod
  def update(self, market: Market) -> Market:

    pass

  @abstractmethod
  def delete(self, market: Market) -> bool:

    pass
