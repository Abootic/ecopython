from abc import ABC, abstractmethod
from typing import List, Optional
from api.dto.market_dto import MarketDTO


class IMarketService(ABC):
  @abstractmethod
  def get_by_id(self, market_id: int) -> Optional[MarketDTO]:
    pass

  @abstractmethod
  def all(self) -> List[MarketDTO]:
    pass

  @abstractmethod
  def add(self, market_dto: MarketDTO) -> MarketDTO:
    pass

  @abstractmethod
  def update(self, market_dto: MarketDTO) -> MarketDTO:
    pass

  @abstractmethod
  def delete(self, market_dto: MarketDTO) -> bool:
    pass
