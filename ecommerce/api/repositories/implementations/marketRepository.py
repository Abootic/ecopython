from typing import List, Optional
from api.repositories.interfaces.ImarketRepository import IMarketRepository
from api.models.market import Market

class MarketRepository(IMarketRepository):

  def get_by_id(self, market_id: int) -> Optional[Market]:
    try:
      return Market.objects.get(id=market_id)
    except Market.DoesNotExist:
      return None

  def all(self) -> List[Market]:
    return Market.objects.all()

  def add(self, market: Market) -> Market:
    if market.pk is None:
        market.save()
        return market
    else:
        raise ValueError("Market already exists. Use update market to update an existing market.")

  def update(self, market: Market) -> Market:
    if market.pk is not None:
        market.save()
        return market
    else:
        raise ValueError("Market does not exist. Use add market to add a new market.")

  def delete(self, market: Market) -> bool:
    if market:
        market.delete()
        return True
    return False
