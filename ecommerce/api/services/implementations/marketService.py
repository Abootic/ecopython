from api.services.interfaces.ImarketService import IMarketService
from api.repositories.interfaces.ImarketRepository import IMarketRepository
from api.models.market import Market
from api.dto.market_dto import MarketDTO
from api.wrpper.result import ConcreteResultT, ResultT
from typing import List, Optional

class MarketService(IMarketService):
    def __init__(self, market_repository: IMarketRepository):
        self.market_repository = market_repository

    def get_by_id(self, market_id: int) -> ResultT:
        try:
            market = self.market_repository.get_by_id(market_id)
            if market:
                market_dto = MarketDTO.from_model(market)
                return ConcreteResultT.success(market_dto)
            return ConcreteResultT.fail("Market not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving market: {str(e)}", 500)

    def all(self) -> ResultT:
        try:
            markets = self.market_repository.all()
            if markets:
                market_dtos = [MarketDTO.from_model(market) for market in markets]
                return ConcreteResultT.success(market_dtos)
            return ConcreteResultT.fail("No markets found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error retrieving markets: {str(e)}", 500)

    def add(self, market_dto: MarketDTO) -> ResultT:
        try:
            market = Market(name=market_dto.name)
            added_market = self.market_repository.add(market)
            if added_market:
                added_market_dto = MarketDTO.from_model(added_market)
                return ConcreteResultT.success(added_market_dto)
            return ConcreteResultT.fail("Failed to add market", 500)
        except Exception as e:
            return ConcreteResultT.fail(f"Error adding market: {str(e)}", 500)

    def update(self, market_dto: MarketDTO) -> ResultT:
        try:
            market = Market(id=market_dto.id, name=market_dto.name)
            updated_market = self.market_repository.update(market)
            if updated_market:
                updated_market_dto = MarketDTO.from_model(updated_market)
                return ConcreteResultT.success(updated_market_dto)
            return ConcreteResultT.fail("Failed to update market", 500)
        except Exception as e:
            return ConcreteResultT.fail(f"Error updating market: {str(e)}", 500)

    def delete(self, market_dto: MarketDTO) -> ResultT:
        try:
            market = Market.objects.get(id=market_dto.id)
            if self.market_repository.delete(market):
                return ConcreteResultT.success("Market successfully deleted", 200)
            return ConcreteResultT.fail("Failed to delete market", 400)
        except Market.DoesNotExist:
            return ConcreteResultT.fail("Market not found", 404)
        except Exception as e:
            return ConcreteResultT.fail(f"Error occurred during deletion: {str(e)}", 500)
